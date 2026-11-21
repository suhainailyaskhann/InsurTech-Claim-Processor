import csv
import json
import os


class ProcessingEngine:
    def __init__(self, json_path="data/claims.json", csv_path="data/reports.csv"):
        self.__json_path = json_path
        self.__csv_path = csv_path
        os.makedirs(os.path.dirname(self.__json_path), exist_ok=True)

    def bubble_sort_by_payout(self, claims):
        """Sorts a list of Claim objects in descending order of payout."""
        arr = list(claims)
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j].calculate_payout() < arr[j + 1].calculate_payout():
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def binary_search_by_id(self, claims, target_id):
        """Finds a Claim by unique ID. Sorts by ID first to guarantee binary search works."""
        sorted_claims = sorted(claims, key=lambda c: c.get_claim_id())
        low = 0
        high = len(sorted_claims) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_id = sorted_claims[mid].get_claim_id()
            if mid_id == target_id:
                return sorted_claims[mid]
            elif mid_id < target_id:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def save_approved_claims_json(self, claims):
        """Saves approved claims to JSON for reloads."""
        data = [c.to_dict() for c in claims]
        with open(self.__json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_approved_claims_json(self):
        """Loads previously saved approved claims from JSON."""
        if not os.path.exists(self.__json_path):
            return []
        with open(self.__json_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []

    def export_monthly_report_csv(self, claims):
        """Exports all processed claims to a CSV report."""
        fieldnames = ["claim_id", "type", "customer_name", "claim_amount", "payout", "status"]
        with open(self.__csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for claim in claims:
                writer.writerow(claim.to_dict())
                