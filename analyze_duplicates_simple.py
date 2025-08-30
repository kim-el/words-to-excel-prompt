#!/usr/bin/env python3
import csv
from collections import Counter, defaultdict

def analyze_zendesk_duplicates(csv_file):
    print("Loading CSV file...")
    
    subjects = []
    requester_ids = []
    from_addresses = []
    subject_requester_pairs = []
    
    # Read the CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        total_rows = 0
        
        for row in reader:
            total_rows += 1
            if total_rows % 50000 == 0:
                print(f"Processed {total_rows:,} rows...")
                
            subject = row.get('subject', '').strip('"')
            requester_id = row.get('requester_id', '').strip('"')
            from_addr = row.get('via.source.from.address', '').strip('"')
            
            if subject:
                subjects.append(subject)
            if requester_id:
                requester_ids.append(requester_id)
            if from_addr and '@' in from_addr:
                from_addresses.append(from_addr)
            if subject and requester_id:
                subject_requester_pairs.append((subject, requester_id))
    
    print(f"Total tickets processed: {total_rows:,}")
    
    # Analyze duplicate subjects
    print("\n=== DUPLICATE SUBJECTS ===")
    subject_counts = Counter(subjects)
    duplicates = [(subject, count) for subject, count in subject_counts.most_common() if count > 1]
    print(f"Subjects with duplicates: {len(duplicates)}")
    print("Top 10 duplicate subjects:")
    for subject, count in duplicates[:10]:
        if subject.strip():
            display_subject = subject[:80] + "..." if len(subject) > 80 else subject
            print(f"  {count:3d}x: {display_subject}")
    
    # Analyze users with multiple tickets
    print("\n=== USERS WITH MULTIPLE TICKETS (by requester_id) ===")
    requester_counts = Counter(requester_ids)
    repeat_requesters = [(req_id, count) for req_id, count in requester_counts.most_common() if count > 1]
    print(f"Requester IDs with multiple tickets: {len(repeat_requesters)}")
    print("Top 10 repeat requesters:")
    for req_id, count in repeat_requesters[:10]:
        print(f"  {count:3d}x: {req_id}")
    
    # Analyze by email if available
    if from_addresses:
        print("\n=== USERS WITH MULTIPLE TICKETS (by email) ===")
        email_counts = Counter(from_addresses)
        repeat_emails = [(email, count) for email, count in email_counts.most_common() if count > 1]
        print(f"Email addresses with multiple tickets: {len(repeat_emails)}")
        print("Top 10 repeat email users:")
        for email, count in repeat_emails[:10]:
            print(f"  {count:3d}x: {email}")
    
    # Find exact duplicates (same subject + same requester)
    print("\n=== EXACT DUPLICATES (Same Subject + Same User) ===")
    pair_counts = Counter(subject_requester_pairs)
    exact_duplicates = [(pair, count) for pair, count in pair_counts.most_common() if count > 1]
    print(f"Exact duplicate combinations: {len(exact_duplicates)}")
    
    if exact_duplicates:
        print("Top 10 exact duplicates:")
        for (subject, req_id), count in exact_duplicates[:10]:
            subject_short = subject[:60] + "..." if len(subject) > 60 else subject
            print(f"  {count:3d}x: {subject_short} (User: {req_id})")
    
    # Summary stats
    print("\n=== SUMMARY ===")
    print(f"Total tickets: {total_rows:,}")
    print(f"Unique subjects: {len(set(subjects)):,}")
    print(f"Unique requesters: {len(set(requester_ids)):,}")
    if requester_ids:
        print(f"Average tickets per user: {len(requester_ids)/len(set(requester_ids)):.1f}")
    
    return duplicates, repeat_requesters, exact_duplicates

if __name__ == "__main__":
    csv_file = "/Users/kimen/Downloads/zendesk_tickets_20250701_121929.csv"
    analyze_zendesk_duplicates(csv_file)