#!/usr/bin/env python
"""
Run database migrations.
Usage: python run_migrations.py upgrade
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    from flask import Flask
    from flask_migrate import Migrate, upgrade
    from config import db
    from app import create_app

    app = create_app()
    
    with app.app_context():
        # Run upgrade command
        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == 'upgrade':
                print("Running database migrations...")
                try:
                    upgrade()
                    print("SUCCESS: Migrations completed successfully!")
                except Exception as e:
                    print(f"ERROR: {str(e)}")
                    sys.exit(1)
            else:
                print(f"Unknown command: {command}")
                print("Available commands: upgrade")
        else:
            print("Running database migrations...")
            try:
                upgrade()
                print("SUCCESS: Migrations completed!")
            except Exception as e:
                print(f"ERROR: {str(e)}")
                sys.exit(1)

