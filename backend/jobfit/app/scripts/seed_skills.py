#!/usr/bin/env python3
"""
Script to seed the skills table from skills_seed.yml.
"""
import asyncio
import os
from pathlib import Path

import yaml
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models import Skill, SkillCategory


# Load database URL from environment or use default
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://jobfit:jobfit@localhost:5432/jobfit_copilot"
)


def load_skills_from_yaml() -> list[dict]:
    """Load skills from the YAML seed file."""
    seed_file = Path(__file__).parent.parent / "data" / "skills_seed.yml"
    
    with open(seed_file, "r") as f:
        data = yaml.safe_load(f)
    
    return data.get("skills", [])


async def seed_skills():
    """Seed the skills table from YAML."""
    # Create async engine and session
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    skills_data = load_skills_from_yaml()
    print(f"Found {len(skills_data)} skills in seed file")
    
    async with async_session() as session:
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for skill_data in skills_data:
            canonical_name = skill_data.get("canonical_name")
            
            # Check if skill already exists
            result = await session.execute(
                select(Skill).where(Skill.canonical_name == canonical_name)
            )
            existing_skill = result.scalar_one_or_none()
            
            if existing_skill:
                # Update existing skill
                existing_skill.display_name = skill_data.get("display_name", canonical_name)
                existing_skill.category = SkillCategory(skill_data.get("category", "other"))
                existing_skill.subcategory = skill_data.get("subcategory")
                existing_skill.aliases = skill_data.get("aliases", [])
                existing_skill.related_skills = skill_data.get("related_skills", [])
                existing_skill.is_trending = skill_data.get("is_trending", False)
                updated_count += 1
            else:
                # Create new skill
                try:
                    category = SkillCategory(skill_data.get("category", "other"))
                except ValueError:
                    print(f"Warning: Unknown category '{skill_data.get('category')}' for {canonical_name}, using 'other'")
                    category = SkillCategory.OTHER
                
                skill = Skill(
                    canonical_name=canonical_name,
                    display_name=skill_data.get("display_name", canonical_name),
                    category=category,
                    subcategory=skill_data.get("subcategory"),
                    aliases=skill_data.get("aliases", []),
                    related_skills=skill_data.get("related_skills", []),
                    is_trending=skill_data.get("is_trending", False),
                )
                session.add(skill)
                created_count += 1
        
        await session.commit()
        
        print(f"\nSeeding complete!")
        print(f"   Created: {created_count}")
        print(f"   Updated: {updated_count}")
        print(f"   Skipped: {skipped_count}")


async def clear_skills():
    """Clear all skills from the database."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        await session.execute(Skill.__table__.delete())
        await session.commit()
        print("All skills cleared")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        asyncio.run(clear_skills())
    else:
        asyncio.run(seed_skills())