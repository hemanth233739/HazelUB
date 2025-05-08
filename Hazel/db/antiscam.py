from Hazel import DATABASE
from pyrogram.types import User

db = DATABASE["antiscam"]

class AntiScam:
  def __init__(self):
    self.escrowers = {}
  
  async def load_escrowers(self, you: int):
    data = await db.find_one({"_id": you}) or {}
    self.escrowers[you] = {escrower["id"]: escrower["name"] for escrower in data.get("escrowers", [])}
  
  async def on(self, you: int):
    await db.update_one({"_id": you}, {"$set": {"status": True}})
  
  async def off(self, you: int):
    await db.update_one({"_id": you}, {"$set": {"status": False}}, upsert=True)
  
  async def is_on(self, you: int) -> bool:
    data = await db.find_one({"_id": you})
    return data.get("status", False) if data else False
  
  async def add_escrower(self, escrower: User, you: int):
    if not isinstance(escrower, User):
      raise TypeError("escrower must be a pyrogram.types.User")
    if you not in self.escrowers:
      await self.load_escrowers(you)
    self.escrowers.setdefault(you, {})[escrower.id] = escrower.first_name
    await db.update_one(
      {"_id": you},
      {"$addToSet": {"escrowers": {"id": escrower.id, "name": escrower.first_name}}},
      upsert=True
    )
  
  async def remove_escrower(self, escrower_id: int, you: int):
    if escrower_id in self.escrowers.get(you, {}):
      del self.escrowers[you][escrower_id]
    await db.update_one(
      {"_id": you},
      {"$pull": {"escrowers": {"id": escrower_id}}}
    )
  
  def list_escrowers(self, you: int) -> dict:
    return self.escrowers.get(you, {})
  
  async def check_for_clones(self, they: User, you: int) -> bool:
    if not isinstance(they, User):
      raise TypeError("they must be a pyrogram.types.User")
    
    if you not in self.escrowers:
      await self.load_escrowers(you)
    
    if they.id in self.escrowers[you]:
      if self.escrowers[you][they.id] != they.first_name:
        self.escrowers[you][they.id] = they.first_name
        await db.update_one(
          {"_id": you, "escrowers.id": they.id},
          {"$set": {"escrowers.$.name": they.first_name}}
        )
        return False
      
      return False   
    for escrower_id, escrower_name in self.escrowers[you].items():
      if escrower_name == they.first_name and escrower_id != they.id:
        return True    
    return False
antiscam = AntiScam()