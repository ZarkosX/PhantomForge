"""
PHANTOMFORGE v3.1 - REAL ACCOUNT CLONER (401 FIXED)
Developer: Shadow V888 | For: Fox
Run: python PhantomForge.py
"""

import discord
import asyncio
import os
import aiohttp

# === حسابك الحقيقي فقط ===
client = discord.Client(intents=discord.Intents.all())

async def clone_server(source_id, target_id):
    source = client.get_guild(source_id)
    target = client.get_guild(target_id)

    if not source or not target:
        print("[-] Server not found. Check IDs.")
        return

    print(f"[Phantom] Cloning: {source.name} → {target.name}")

    # مسح السيرفر الهدف
    print("[Phantom] Clearing target...")
    for ch in list(target.channels):
        try: await ch.delete()
        except: pass
    for role in target.roles[1:]:
        try: await role.delete()
        except: pass

    # نسخ الشعار
    if source.icon:
        async with aiohttp.ClientSession() as s:
            async with s.get(source.icon.url) as r:
                await target.edit(icon=await r.read())
        print("[Phantom] Icon cloned")

    # نسخ الإيموجي
    print("[Phantom] Cloning emojis...")
    for emoji in source.emojis:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(emoji.url) as r:
                    await target.create_custom_emoji(name=emoji.name, image=await r.read())
            print(f"   [Emoji] {emoji.name}")
        except: pass

    # نسخ الرتب
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

    # نسخ القنوات
    print("[Phantom] Cloning channels...")
    cat_map = {}
    for ch in source.channels:
        try:
            if isinstance(ch, discord.CategoryChannel):
                new_cat = await target.create_category(name=ch.name)
                for t, p in ch.overwrites.items():
                    nt = role_map.get(t.id)
                    if nt: await new_cat.set_permissions(nt, overwrite=p)
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

            for t, p in ch.overwrites.items():
                nt = role_map.get(t.id)
                if nt: await new_ch.set_permissions(nt, overwrite=p)

            print(f"   [Ch] {ch.name}")
        except Exception as e:
            print(f"   [-] {e}")

    print(f"\n[Shadow] SERVER CLONED 100%")
    print(f"[Shadow] {source.name} → {target.name}")

def run():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("     PHANTOMFORGE - REAL ACCOUNT CLONER")
    print("       Get Token from Network Tab")
    print("="*60)

    print("\n[INFO] Open Discord → F12 → Network → Send message → Copy Authorization")
    token = input("\n[?] Your Token: ").strip()

    if not token:
        print("[!] Token cannot be empty!")
        return

    try:
        src = int(input("[?] Source Server ID: ").strip())
        dst = int(input("[?] Target Server ID: ").strip())
    except:
        print("[!] Invalid ID format!")
        return

    @client.event
    async def on_connect():
        print(f"\n[Phantom] Logged in: {client.user}")
        await clone_server(src, dst)
        await client.close()

    try:
        client.run(token, log_handler=None)
    except discord.LoginFailure:
        print("\n[!] LOGIN FAILED: Invalid/expired token")
        print("    → Get fresh token from Network tab")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    run()
