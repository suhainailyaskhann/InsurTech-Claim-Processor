from models.claims import HealthClaim, AutoClaim, PropertyClaim
from models.exceptions import InvalidClaimAmountError, PolicyExpiredException
from core.data_structures import ClaimQueue, AppealStack, ClaimHistoryList
from core.processing_engine import ProcessingEngine


def create_claim():
    try:
        claim_id = int(input("Enter Claim ID (numeric): "))
        name = input("Enter Customer Name: ")
        amount = float(input("Enter Claim Amount: "))
        active_input = input("Is policy active? (y/n): ").strip().lower()
        is_active = active_input == "y"

        print("Claim Type: 1. Health  2. Auto  3. Property")
        c_type = input("Select type (1-3): ").strip()

        if c_type == "1":
            return HealthClaim(claim_id, name, amount, is_active)
        elif c_type == "2":
            return AutoClaim(claim_id, name, amount, is_active)
        elif c_type == "3":
            return PropertyClaim(claim_id, name, amount, is_active)
        else:
            print("Invalid claim type.")
            return None
    except (InvalidClaimAmountError, PolicyExpiredException) as e:
        print(f"Validation Error: {e}")
        return None
    except ValueError:
        print("Invalid numeric input.")
        return None


def main():
    pending_queue = ClaimQueue()
    appeal_stack = AppealStack()
    history_list = ClaimHistoryList()
    engine = ProcessingEngine()
    approved_claims = []

    while True:
        print("\n=== InsurTech Automated Claim Processor ===")
        print("1. Submit New Claim (Enqueue)")
        print("2. Process Next Pending Claim (Dequeue)")
        print("3. Review Latest Appeal (Pop Stack)")
        print("4. Rank Pending Claims by Payout (Bubble Sort)")
        print("5. Search Claim History by ID (Binary Search)")
        print("6. Save Approved Claims (JSON) & Export Report (CSV)")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            claim = create_claim()
            if claim:
                pending_queue.enqueue(claim)
                history_list.append(claim)
                print(f"Claim #{claim.get_claim_id()} added to queue. Estimated Payout: ${claim.calculate_payout()}")

        elif choice == "2":
            claim = pending_queue.dequeue()
            if not claim:
                print("No pending claims in queue.")
                continue
            print(f"Processing Claim #{claim.get_claim_id()} ({claim.get_customer_name()}) - Payout: ${claim.calculate_payout()}")
            decision = input("Approve (a) or Deny (d)? ").strip().lower()
            if decision == "a":
                claim.set_status("Approved")
                approved_claims.append(claim)
                print("Claim Approved.")
            else:
                claim.set_status("Denied")
                appeal_stack.push(claim)
                print("Claim Denied and pushed to Appeals Stack.")

        elif choice == "3":
            claim = appeal_stack.pop()
            if not claim:
                print("No appeals in stack.")
                continue
            print(f"Reviewing Appeal for Claim #{claim.get_claim_id()} ({claim.get_customer_name()})")
            overturn = input("Overturn and Approve? (y/n): ").strip().lower()
            if overturn == "y":
                claim.set_status("Approved (Appeal)")
                approved_claims.append(claim)
                print("Appeal Approved.")
            else:
                claim.set_status("Permanently Denied")
                print("Denial upheld.")

        elif choice == "4":
            pending = pending_queue.get_all()
            if not pending:
                print("No pending claims to sort.")
                continue
            ranked = engine.bubble_sort_by_payout(pending)
            print("\n--- Pending Claims Ranked by Payout ---")
            for c in ranked:
                print(f"ID: {c.get_claim_id()} | {c.get_customer_name()} | Payout: ${c.calculate_payout()}")

        elif choice == "5":
            try:
                target_id = int(input("Enter Claim ID to search: "))
                found = engine.binary_search_by_id(history_list.get_all(), target_id)
                if found:
                    print(f"Found: {found.to_dict()}")
                else:
                    print("Claim ID not found.")
            except ValueError:
                print("Please enter a valid numeric ID.")

        elif choice == "6":
            engine.save_approved_claims_json(approved_claims)
            engine.export_monthly_report_csv(history_list.get_all())
            print("Saved approved claims to data/claims.json and exported report to data/reports.csv.")

        elif choice == "7":
            print("Exiting InsurTech.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
