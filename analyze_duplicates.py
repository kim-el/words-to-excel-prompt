#!/usr/bin/env python3
import csv
import pandas as pd
from collections import Counter, defaultdict

def analyze_zendesk_duplicates(csv_file):
    print("Loading CSV file...")
    
    # Read the CSV file
    df = pd.read_csv(csv_file, low_memory=False)
    
    print(f"Total tickets: {len(df):,}")
    
    # Analyze duplicate subjects
    print("\n=== DUPLICATE SUBJECTS ===")
    subject_counts = df['subject'].value_counts()
    duplicates = subject_counts[subject_counts > 1]
    print(f"Subjects with duplicates: {len(duplicates)}")
    print("Top 10 duplicate subjects:")
    for subject, count in duplicates.head(10).items():
        if pd.notna(subject) and subject.strip():
            print(f"  {count:3d}x: {subject[:80]}...")
    
    # Analyze by requester email (via.source.from.address)
    print("\n=== USERS WITH MULTIPLE TICKETS ===")
    if 'via.source.from.address' in df.columns:
        email_counts = df['via.source.from.address'].value_counts()
        repeat_users = email_counts[email_counts > 1]
        print(f"Users with multiple tickets: {len(repeat_users)}")
        print("Top 10 repeat users:")
        for email, count in repeat_users.head(10).items():
            if pd.notna(email) and '@' in str(email):
                print(f"  {count:3d}x: {email}")
    
    # Analyze requester_id for repeat users
    print("\n=== REQUESTER IDs WITH MULTIPLE TICKETS ===")
    requester_counts = df['requester_id'].value_counts()
    repeat_requesters = requester_counts[requester_counts > 1]
    print(f"Requester IDs with multiple tickets: {len(repeat_requesters)}")
    print("Top 10 repeat requesters:")
    for req_id, count in repeat_requesters.head(10).items():
        if pd.notna(req_id):
            print(f"  {count:3d}x: {req_id}")
    
    # Find exact duplicate tickets (same subject + same requester)
    print("\n=== EXACT DUPLICATES (Same Subject + Same User) ===")
    df_clean = df.dropna(subset=['subject', 'requester_id'])
    duplicate_pairs = df_clean.groupby(['subject', 'requester_id']).size()
    exact_duplicates = duplicate_pairs[duplicate_pairs > 1]
    print(f"Exact duplicate combinations: {len(exact_duplicates)}")
    
    if len(exact_duplicates) > 0:
        print("Top 10 exact duplicates:")
        for (subject, req_id), count in exact_duplicates.head(10).items():
            subject_short = subject[:60] + "..." if len(str(subject)) > 60 else subject
            print(f"  {count:3d}x: {subject_short} (User: {req_id})")
    
    # Summary stats
    print("\n=== SUMMARY ===")
    print(f"Total tickets: {len(df):,}")
    print(f"Unique subjects: {df['subject'].nunique():,}")
    print(f"Unique requesters: {df['requester_id'].nunique():,}")
    print(f"Average tickets per user: {len(df)/df['requester_id'].nunique():.1f}")
    
    return df

if __name__ == "__main__":
    csv_file = "/Users/kimen/Downloads/zendesk_tickets_20250701_121929.csv"
    analyze_zendesk_duplicates(csv_file)