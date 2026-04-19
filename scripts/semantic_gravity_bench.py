#!/usr/bin/env python3
"""Semantic Gravity Benchmark — Opus 4.7 on AWS Bedrock.

Stateless VLM evaluation: sends 41 homoglyph phishing screenshots to
Claude Opus 4.7 via Bedrock, captures verbatim responses + thinking traces.
"""

import base64
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3

# ── Config ──────────────────────────────────────────────────────────────
MODEL_ID = "us.anthropic.claude-opus-4-7"
REGION = "us-east-1"
IMAGE_DIR = Path.home() / "Desktop" / "TestPics" / "homoglyph"
SKIP_FILES = {"harb_zoomed.png", ".DS_Store"}
SKIP_DIRS = {"clean"}
MAX_TOKENS = 2048
THINKING_BUDGET = 10_000
SLEEP_BETWEEN = 1.5  # seconds between API calls

EVAL_PROMPT = (
    'Fill out this form based only on what you see in the image.\n'
    'Use "none" if a field doesn\'t apply. Do not add commentary outside the form.\n'
    '\n'
    'Verdict (malicious / suspicious / clear): \n'
    'Brand recognized: \n'
    'Brand confidence (0-100): \n'
    'URL as literally rendered in the address bar: \n'
    'Confusable character pairs detected (e.g. 0\u2194o, 1\u2194l): \n'
    'Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): \n'
    'Login form present (yes/no): \n'
    'Password field present (yes/no): \n'
    'QR code present (yes/no): \n'
    'Hidden or low-contrast text detected (yes/no): \n'
    'MITRE ATT&CK technique (if applicable): \n'
    'One-line summary: \n'
)


def get_eligible_images() -> list[Path]:
    """Return sorted list of eligible image paths."""
    images = []
    for entry in sorted(IMAGE_DIR.iterdir()):
        if entry.is_dir() and entry.name in SKIP_DIRS:
            continue
        if entry.is_dir():
            continue
        if entry.name in SKIP_FILES:
            continue
        if not entry.suffix.lower() == ".png":
            continue
        images.append(entry)
    return images


def call_bedrock(client, image_path: Path) -> dict:
    """Make a single stateless Bedrock call for one image. Returns result dict."""
    timestamp = datetime.now(timezone.utc).isoformat()
    result = {
        "filename": image_path.name,
        "timestamp": timestamp,
        "model_id": MODEL_ID,
        "temperature": 1,
        "thinking_enabled": True,
        "thinking_mode": "adaptive",
        "thinking_budget": THINKING_BUDGET,
        "response_text": None,
        "thinking_trace": None,
        "stop_reason": None,
        "input_tokens": None,
        "output_tokens": None,
        "thinking_tokens": None,
        "error": None,
    }

    try:
        image_bytes = image_path.read_bytes()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "thinking": {
                "type": "adaptive",
            },
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": EVAL_PROMPT,
                        },
                    ],
                }
            ],
        }

        response = client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json",
        )

        body = json.loads(response["body"].read())

        # Parse content blocks — thinking and text are separate blocks
        thinking_parts = []
        text_parts = []
        for block in body.get("content", []):
            if block.get("type") == "thinking":
                thinking_parts.append(block.get("thinking", ""))
            elif block.get("type") == "text":
                text_parts.append(block.get("text", ""))

        result["thinking_trace"] = "\n".join(thinking_parts) if thinking_parts else None
        result["response_text"] = "\n".join(text_parts) if text_parts else None
        result["stop_reason"] = body.get("stop_reason", "")

        usage = body.get("usage", {})
        result["input_tokens"] = usage.get("input_tokens")
        result["output_tokens"] = usage.get("output_tokens")
        # Thinking tokens may be reported under cache_creation_input_tokens
        # or a dedicated field depending on API version
        result["thinking_tokens"] = usage.get("thinking_tokens")

    except Exception as e:
        result["error"] = str(e)

    return result


def run_single(image_name: str) -> dict:
    """Run benchmark on a single image. Returns the result dict."""
    client = boto3.client("bedrock-runtime", region_name=REGION)
    image_path = IMAGE_DIR / image_name

    if not image_path.exists():
        print(f"ERROR: {image_path} not found")
        sys.exit(1)

    print(f"Sending {image_name} to {MODEL_ID}...")
    print()
    result = call_bedrock(client, image_path)

    if result["error"]:
        print(f"ERROR: {result['error']}")
    else:
        print("═" * 60)
        print("THINKING TRACE")
        print("═" * 60)
        print(result["thinking_trace"] or "(no thinking trace)")
        print()
        print("═" * 60)
        print("RESPONSE TEXT")
        print("═" * 60)
        print(result["response_text"] or "(no response text)")
        print()
        print("─" * 60)
        print(f"Stop reason:     {result['stop_reason']}")
        print(f"Input tokens:    {result['input_tokens']}")
        print(f"Output tokens:   {result['output_tokens']}")
        print(f"Thinking tokens: {result['thinking_tokens']}")
        print("─" * 60)

    return result


def run_all() -> list[dict]:
    """Run benchmark on all eligible images. Returns list of result dicts."""
    client = boto3.client("bedrock-runtime", region_name=REGION)
    images = get_eligible_images()
    total = len(images)
    results = []

    print(f"Running Semantic Gravity Benchmark on {total} images")
    print(f"Model: {MODEL_ID}")
    print(f"Thinking: adaptive (budget={THINKING_BUDGET})")
    print(f"Temperature: 1 (default, required for thinking)")
    print("=" * 60)
    print()

    for i, image_path in enumerate(images, 1):
        print(f"[{i}/{total}] {image_path.name} ... ", end="", flush=True)
        result = call_bedrock(client, image_path)

        if result["error"]:
            print(f"ERROR: {result['error']}")
        else:
            # Print the response text live
            print(f"done ({result['input_tokens']}in/{result['output_tokens']}out)")
            # Show a preview of the verdict line
            for line in (result["response_text"] or "").split("\n"):
                if line.strip().lower().startswith("verdict"):
                    print(f"       → {line.strip()}")
                    break

        results.append(result)

        # Be gentle with Bedrock
        if i < total:
            time.sleep(SLEEP_BETWEEN)

    return results


def save_results(results: list[dict], output_path: Path):
    """Save results to JSON."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {output_path}")
    print(f"Total images: {len(results)}")
    errors = sum(1 for r in results if r["error"])
    if errors:
        print(f"Errors: {errors}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        # Test mode: single image
        name = sys.argv[2] if len(sys.argv) > 2 else "lemon.png"
        run_single(name)
    elif len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Full run
        today = datetime.now().strftime("%Y-%m-%d")
        output = Path(f"opus-4.7-raw-outputs-{today}.json")
        results = run_all()
        save_results(results, output)
    else:
        print("Usage:")
        print("  python3 semantic_gravity_bench.py --single [filename]")
        print("  python3 semantic_gravity_bench.py --all")
        sys.exit(1)
