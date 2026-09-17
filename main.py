from dataset import Dataset

def main():
    file_path = "messy_people.csv"
    record_list = []
    reasons = {}
    
    dataset = Dataset(file_path, record_list, reasons)

    # handle duplicate IDs
    dataset.handle_id()

    print("\n========= Elapsed time summary for each function =========")
    print("----------------------------------------------------------\n")

    # generate complete report
    summary = dataset.summary_report()

    # generate a text file with summary
    dataset.save_report(summary)

    print("\n\n================= DATASET SUMMARY REPORT =================")
    print("----------------------------------------------------------\n")
    print(f"Rows loaded: {summary['rows_loaded']}")
    print(f"Rows dropped: {summary['rows_dropped']}")

    print("\nReasons dropped (where each row was dropped):")
    print("---------------------------------------------")
    for reason, count in summary["reasons"].items():
        print(f"  {reason}: {count}")

    print("\nKey statistics:")
    print("----------------")
    print(f"  Average score: {summary['key_stats']['average_score']}\n")
    print(f"  Oldest person: {summary['key_stats']['oldest_person']}\n")
    print(f"  Youngest person: {summary['key_stats']['youngest_person']}\n")
    print(f"  People per city: {summary['key_stats']['people_per_city']}\n")

    print(f"Final cleaned records: {len(dataset.records)}\n")
    print("====================== END OF SUMMARY ======================\n")
    

if __name__ == '__main__':
    main() 