
import json
import logging
from datetime import datetime
from pathlib import Path

from backend.state import AgricultureState

# File locations
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "mandi_prices.json"
LOG_FILE = Path(__file__).with_name("market_agent.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_market_data():
    """Load market records from the JSON file."""

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        logging.error("mandi_prices.json not found")
        raise

    except json.JSONDecodeError:
        logging.error("Invalid JSON format")
        raise


def parse_date(date_string):
    """Convert DD/MM/YYYY into a date object."""

    try:
        return datetime.strptime(date_string, "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return None


def get_market_data(crop_name, state=None, district=None, limit=5):
    """
    Retrieve market information for a recommended crop.

    Optional filters:
    state: Filter by state
    district: Filter by district
    limit: Maximum number of market records returned
    """

    crop = crop_name.strip().lower()

    logging.info("Market lookup started for crop: %s", crop)

    try:
        market_data = load_market_data()

        if crop not in market_data:
            return {
                "status": "error",
                "crop": crop,
                "message": "Crop not supported by market module."
            }

        records = market_data[crop]

        # Apply optional location filters
        if state:
            records = [
                r for r in records
                if r.get("state", "").lower() == state.lower()
            ]

        if district:
            records = [
                r for r in records
                if r.get("district", "").lower() == district.lower()
            ]

        if not records:
            logging.warning("No market records found for %s", crop)

            return {
                "status": "no_data",
                "crop": crop,
                "records_count": 0,
                "markets": [],
                "demand_data": None,
                "message": "No market price records available for this crop or location."
            }

        # Sort records by arrival date, newest first
        records = sorted(
            records,
            key=lambda r: parse_date(r.get("arrival_date")) or datetime.min.date(),
            reverse=True
        )

        # Use records from the latest available date for the price summary
        latest_date = parse_date(records[0].get("arrival_date"))

        latest_records = [
            r for r in records
            if parse_date(r.get("arrival_date")) == latest_date
        ]

        prices = [
            r["modal_price"]
            for r in latest_records
            if isinstance(r.get("modal_price"), (int, float))
            and r["modal_price"] > 0
        ]

        average_price = (
            round(sum(prices) / len(prices), 2)
            if prices else None
        )

        result = {
            "status": "success",
            "crop": crop,
            "records_count": len(records),
            "latest_arrival_date": (
                latest_date.strftime("%d/%m/%Y")
                if latest_date else None
            ),
            "average_modal_price": average_price,
            "price_unit": "As reported in source dataset; verify unit metadata",
            "markets": records[:limit],
            "demand_data": None,
            "message": "Market prices retrieved successfully. Demand data is unavailable."
        }

        logging.info(
            "Market lookup successful for %s. Records: %d",
            crop, len(records)
        )

        return result

    except Exception:
        logging.exception("Market lookup failed for %s", crop)

        return {
            "status": "error",
            "crop": crop,
            "message": "An error occurred while retrieving market data."
        }



def run(state: AgricultureState) -> dict:
    """Adapter for integrating the Market Agent with LangGraph."""

    farmer_input = state.get("farmer_input", {})

    crop_name = farmer_input.get("crop_name")
    state_name = farmer_input.get("state")
    district = farmer_input.get("district")

    if not isinstance(crop_name, str) or not crop_name.strip():
        return {
            "market_result": {
                "status": "failed",
                "data": {},
                "summary": "Market analysis requires a farmer-selected crop.",
                "warnings": ["Missing or invalid input: crop_name."]
            }
        }

    result = get_market_data(
        crop_name=crop_name,
        state=state_name,
        district=district
    )

    status = "success" if result.get("status") == "success" else "failed"

    warnings = []

    if result.get("demand_data") is None:
        warnings.append("Demand data is unavailable.")

    if result.get("status") == "no_data":
        warnings.append("No market records were found for this crop or location.")

    if result.get("status") == "error":
        warnings.append(result.get("message", "Market lookup failed."))

    return {
        "market_result": {
            "status": status,
            "data": result,
            "summary": result.get("message", "Market analysis completed."),
            "warnings": warnings
        }
    }


# Run a simple test when this file is executed directly
if __name__ == "__main__":
    print("MARKET AGENT STARTED")

    crop = input("Enter crop name: ").strip()
    result = get_market_data(crop)

    print("\nMARKET RESULT:")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    print("\nCheck market_agent.log for execution details.")
