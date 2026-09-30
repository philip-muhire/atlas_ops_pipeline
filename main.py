import argparse
from pathlib import Path
from src.ingestion import parse_crm_csv, parse_billing_json
from src.pipeline import deduplicate_customers, deduplicate_orders


def main():
    parser = argparse.ArgumentParser(
        description="Atlas Ops Data Ingestion & Reconciliation Pipeline"
    )

    parser.add_argument(
        "--crm",
        type=str,
        help="Path to CRM CSV export file"
    )
    parser.add_argument(
        "--billing",
        type=str,
        help="Path to Billing JSON export file"
    )

    args = parser.parse_args()

    if args.crm:
        crm_path = Path(args.crm)
        print(f"\n================ Processing CRM Data: {crm_path} ================")
        raw_customers = parse_crm_csv(crm_path)
        clean_customers = list(deduplicate_customers(raw_customers))
        
        print(f"\nSuccessfully processed {len(clean_customers)} unique customers:")
        for customer in clean_customers:
            print(f"  -> {customer}")

    if args.billing:
        billing_path = Path(args.billing)
        print(f"\n================ Processing Billing Data: {billing_path} ================")
        raw_orders = parse_billing_json(billing_path)
        clean_orders = list(deduplicate_orders(raw_orders))
        
        print(f"\nSuccessfully processed {len(clean_orders)} unique orders:")
        for order in clean_orders:
            print(f"  -> {order}")

    if not args.crm and not args.billing:
        print("No input files provided. Use --help to see available options.")


if __name__ == "__main__":
    main()
