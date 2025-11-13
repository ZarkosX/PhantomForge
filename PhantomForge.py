"""
PHANTOMFORGE v3.0 - PURE USER ACCOUNT CLONER
Developer: Shadow V888 | For: Fox
Run: python PhantomForge.py
"""

import discord
import asyncio
import os
import aiohttp

# === حسابك الحقيقي فقط – بدون بوت، بدون أي حاجة ===
client = discord.Client(intents=discord.Intents.all())

async def clone_server(source_id, target_id):
    source = client.get_guild(source_id)
    target = client.get_guild(target_id)

    if not source or not target:
        print("[-] Server not found. Check IDs.")
        return

    print(f"[Phantom] Cloning: {source.name} → {target.name}")

    # 1. مسح السيرفر الهدف
    print("[Phantom] Clearing target server...")
    for ch in list(target.channels):
        try: await ch.delete()
        except: pass
    for role in target.roles[1:]:
        try: await role.delete()
        except: pass

    # 2. نسخ الشعار
    if source.icon:
        async with aiohttp.ClientSession() as session:
            async with session.get(source.icon.url) as resp:
                icon_data = await resp.read()
                await target.edit(icon=icon_data)
        print("[Phantom] Icon cloned")

    # 3. نسخ الإيموجي
    print("[Phantom] Cloning emojis...")
    for emoji in source.emojis:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(emoji.url) as resp:
                    img = await resp.read()
                    await target.create_custom_emoji(name=emoji.name, image=img)
            print(f"   [Emoji] {emoji.name}")
        except: pass

    # 4. نسخ الرتب
    role_map = {source.default_role.id: target.default_role}
    print("[Phantom] Cloning roles...")
    for role in reversed(source.roles[1:]):
        try:
            new_role = await target.create_role(
                name=role.name,
                permissions=role.permissions,
                color=role.color,
                hoist=role.hoist,
                mentionable=role.mentionable
            )
            role_map[role.id] = new_role
            print(f"   [Role] {role.name}")
        except: pass

    # 5. نسخ القنوات
    print("[Phantom] Cloning channels...")
    cat_map = {}
    for ch in source.channels:
        try:
            if isinstance(ch, discord.CategoryChannel):
                new_cat = await target.create_category(name=ch.name)
                for target_obj, perm in ch.overwrites.items():
                    mapped = role_map.get(target_obj.id)
                    if mapped:
                        await new_cat.set_permissions(mapped, overwrite=perm)
                cat_map[ch.id] = new_cat
                print(f"   [Cat] {ch.name}")
                continue

            base = {'name': ch.name}
            if isinstance(ch, discord.TextChannel):
                new_ch = await target.create_text_channel(
                    **base,
                    category=cat_map.get(ch.category_id),
                    topic=ch.topic,
                    slowmode_delay=ch.slowmode_delay,
                    nsfw=ch.nsfw
                )
            else:
                new_ch = await target.create_voice_channel(
                    **base,
                    category=cat_map.get(ch.category_id),
                    bitrate=ch.bitrate,
                    user_limit=ch.user_limit
                )

            for target_obj, perm in ch.overwrites.items():
                mapped = role_map.get(target_obj.id)
                if mapped:
                    await new_ch.set_permissions(mapped, overwrite=perm)

            print(f"   [Ch] {ch.name}")
        except Exception as e:
            print(f"   [-] Failed: {e}")

    print(f"\n[Shadow] SERVER CLONED SUCCESSFULLY!")
    print(f"[Shadow] {source.name} → {target.name}")

# === الواجهة البسيطة ===
def run():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("     PHANTOMFORGE - USER ACCOUNT CLONER")
    print("          Works with YOUR REAL ACCOUNT")
    print("="*60)

    token = input("\n[?] Your Discord Token: ").strip()
    src = int(input("[?] Source Server ID: ").strip())
    dst = int(input("[?] Target Server ID: ").strip())

    @client.event
    async def on_connect():
        print(f"\n[Phantom] Logged in as: {client.user}")
        await clone_server(src, dst)
        await client.close()

    # تشغيل بحسابك الحقيقي – بدون أي بوت
    client.run(token, log_handler=None)

if __name__ == "__main__":
    run()
