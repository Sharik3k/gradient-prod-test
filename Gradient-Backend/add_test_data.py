#!/usr/bin/env python3
"""
Add test data to Gmail messages table for demonstration
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from db import conn
from datetime import datetime, timedelta
import json

def add_test_leads():
    """Add test Gmail leads to database"""
    
    test_leads = [
        {
            "gmail_id": "test_msg_001",
            "status": "new",
            "first_name": "Іван",
            "last_name": "Петренко",
            "full_name": "Іван Петренко",
            "email": "ivan.petrenko@example.com",
            "subject": "Запит щодо співпраці",
            "received_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "company": "IT Solutions Ltd",
            "body": "Доброго дня! Цікавить можливість співпраці з вашою компанією.",
            "phone": "+380501234567",
            "website": "itsolutions.example.com",
            "company_name": "IT Solutions Ltd",
            "company_info": "IT-компанія, що спеціалізується на веб-розробці",
            "person_role": "CEO",
            "person_links": "linkedin.com/in/ivanpetrenko",
            "person_location": "Київ, Україна",
            "person_experience": "10 років в IT",
            "person_summary": "Досвідчений керівник з технічним бекграундом",
            "person_insights": "Зацікавлений у партнерстві для розширення бізнесу",
            "company_insights": "Стабільна компанія з хорошою репутацією",
            "is_priority": True,
            "pending_review": False,
            "preprocessing_status": "completed",
            "assigned_to": None,
            "synced_at": datetime.now().isoformat(),
        },
        {
            "gmail_id": "test_msg_002",
            "status": "contacted",
            "first_name": "Олена",
            "last_name": "Ковальчук",
            "full_name": "Олена Ковальчук",
            "email": "olena.k@example.com",
            "subject": "Пропозиція про проект",
            "received_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "company": "Digital Agency",
            "body": "Маємо цікавий проект для вашої команди. Хотіли б обговорити деталі.",
            "phone": "+380639876543",
            "website": "digitalagency.example.com",
            "company_name": "Digital Agency",
            "company_info": "Цифрове маркетингове агентство",
            "person_role": "Project Manager",
            "person_links": "",
            "person_location": "Львів, Україна",
            "person_experience": "5 років в управлінні проектами",
            "person_summary": "Енергійний менеджер з досвідом в IT проектах",
            "person_insights": "Шукає надійного партнера для довгострокової співпраці",
            "company_insights": "Молоде агенство з амбітними проектами",
            "is_priority": False,
            "pending_review": True,
            "preprocessing_status": "completed",
            "assigned_to": None,
            "synced_at": datetime.now().isoformat(),
        },
        {
            "gmail_id": "test_msg_003",
            "status": "new",
            "first_name": "Андрій",
            "last_name": "Мельник",
            "full_name": "Андрій Мельник",
            "email": "andriy.m@example.com",
            "subject": "Питання про послуги",
            "received_at": (datetime.now() - timedelta(days=3)).isoformat(),
            "company": "Startup Hub",
            "body": "Хотів би дізнатися більше про ваші послуги та ціни.",
            "phone": "+380441112233",
            "website": "startuphub.example.com",
            "company_name": "Startup Hub",
            "company_info": "Інкубатор для стартапів",
            "person_role": "Founder",
            "person_links": "twitter.com/andriymelnik",
            "person_location": "Харків, Україна",
            "person_experience": "3 роки в підприємництві",
            "person_summary": "Молодий підприємець з технічною освітою",
            "person_insights": "Планує масштабування бізнесу",
            "company_insights": "Швидкозростаючий стартап",
            "is_priority": True,
            "pending_review": False,
            "preprocessing_status": "completed",
            "assigned_to": None,
            "synced_at": datetime.now().isoformat(),
        }
    ]
    
    print("Adding test leads to database...")
    
    for lead in test_leads:
        try:
            # Check if lead already exists
            existing = conn.execute(
                "SELECT gmail_id FROM gmail_messages WHERE gmail_id = ?",
                [lead["gmail_id"]]
            ).fetchone()
            
            if existing:
                print(f"Lead {lead['gmail_id']} already exists, skipping...")
                continue
            
            # Insert lead
            columns = list(lead.keys())
            placeholders = ", ".join(["?"] * len(columns))
            values = list(lead.values())
            
            conn.execute(
                f"INSERT INTO gmail_messages ({', '.join(columns)}) VALUES ({placeholders})",
                values
            )
            
            print(f"✅ Added lead: {lead['full_name']} ({lead['email']})")
            
        except Exception as e:
            print(f"❌ Error adding lead {lead['gmail_id']}: {e}")
    
    try:
        conn.commit()
        print("\n🎉 Test data added successfully!")
        print(f"Total leads in database: {conn.execute('SELECT COUNT(*) FROM gmail_messages').fetchone()[0]}")
    except Exception as e:
        print(f"❌ Error committing changes: {e}")

if __name__ == "__main__":
    add_test_leads()
