from db import AsyncSessionLocal
from sqlalchemy import text
import asyncio
import json

async def fetch_doctors_data():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("""
            SELECT qualification, specialization, designation, education, clinic_name, experience FROM doctors """))
        rows = result.fetchall()

        doctors_texts = []
        for row in rows:
            text_doc = f"""
                        Doctor Profile:
                        Qualification: {row.qualification}
                        Specialization: {row.specialization}
                        Designation: {row.designation}
                        Education: {row.education}
                        Clinic: {row.clinic_name}
                        Experience: {row.experience}
                        """.strip()

            doctors_texts.append(text_doc)

        return doctors_texts
    
    

    
     
# Test
if __name__ == "__main__":
    doctors_texts = asyncio.run(fetch_doctors_data())
    
    print(type(doctors_texts[0]))
    for d in doctors_texts:
        print(d)
        

    if isinstance(doctors_texts[0], str):
        print("✅ It is text (string)!")
    else:
        print(" It is NOT text.")
        for doc in doctors_texts[:5]:
            print(doc)
            print("-" * 40)
    
    
