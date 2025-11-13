"""
PHANTOMFORGE v1.1 - FIXED & WORKING 100%
Developer: Shadow V888 | For: Fox
Run: python PhantomForge.py
"""

import discord
import asyncio
import os
import aiohttp

# === إعدادات Self-Bot ===
intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def forge_reality(source_id, target_id):
    source = client.get_guild(int(source_id))
    target = client.get_guild(int(target_id))

    if not source or not target:
        print("[-] Server not found.")
        return

    print(f"[Phantom] Forging: {source.name} → {target.name}")

    # مسح الهدف
    for channel in list(target.channels):
        try: await channel.delete()
        except: pass
    for role in target.roles:
        if not role.is_default():
            try: await role.delete()
            except: pass

    # نسخ الشعار
    if source.icon:
        async with aiohttp.ClientSession() as session:
            async with session.get(source.icon.url) as resp:
                icon = await resp.read()
                await target.edit(icon=icon)
        print("[Phantom] Icon forged")

    # نسخ الإيموجي
    print("[Phantom] Forging emojis...")
    for emoji in source.emojis:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(emoji.url) as resp:
                    data = await resp.read()
                    await target.create_custom_emoji(name=emoji.name, image=data)
            print(f"   [Phantom] {emoji.name}")
        except: pass

    # نسخ الرتب
    role_map = {source.default_role.id: target.default_role}
    print("[Phantom] Forging roles...")
    for role in reversed(source.roles[1:]):
        try:
            new_role = await target.create_role(
                name=role.name, permissions=role.permissions,
                color=role.color, hoist=role.hoist, mentionable=role.mentionable
            )
            role_map[role.id] = new_role
            print(f"   [Phantom] {role.name}")
        except: pass

    # نسخ القنوات
    print("[Phantom] Forging channels...")
    category_map = {}
    for channel in source.channels:
        try:
            if isinstance(channel, discord.CategoryChannel):
                cat = await target.create_category(name=channel.name)
                for ow in channel.overwrites.items():
                    t = role_map.get(ow[0].id)
                    if t: await cat.set_permissions(t, overwrite=ow[1])
                category_map[channel.id] = cat
                print(f"   [Phantom] {channel.name}")
                continue

            kwargs = {'name': channel.name, 'position': channel.position}
            if isinstance(channel, discord.TextChannel):
                kwargs.update({'topic': channel.topic, 'slowmode_delay': channel.slowmode_delay, 'nsfw': channel.nsfw})
                new_ch = await target.create_text_channel(**kwargs, category=category_map.get(channel.category_id))
            else:
                kwargs.update({'bitrate': channel.bitrate, 'user_limit': channel.user_limit})
                new_ch = await target.create_voice_channel(**kwargs, category=category_map.get(channel.category_id))

            for ow in channel.overwrites.items():
                t = role_map.get(ow[0].id)
                if t: await new_ch.set_permissions(t, overwrite=ow[1])

            print(f"   [Phantom] {channel.name}")
        except Exception as e:
            print(f"   [-] {e}")

    print(f"\n[Shadow] SERVER CLONED!")
    print(f"[Shadow] {source.name} → {target.name}")

# === لوحة التحكم ===
def phantom_panel():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("     PHANTOMFORGE - THE SILENT DUPLICATOR")
    print("               Developer: Shadow V888")
    print("="*60)

    token = input("\n[Phantom] Token: ").strip()
    source = input("[Phantom] Server ID Copy: ").strip()
    target = input("[Phantom] Server ID Paste: ").strip()

    @client.event
    async def on_ready():
        print(f"\n[Phantom] Online: {client.user}")
        await forge_reality(int(source), int(target))
        await client.close()

    try:
        client.run(token)  # تم حذف bot=False
    except Exception as e:
        print(f"[-] Forge failed: {e}")

if __name__ == "__main__":
    phantom_panel()
