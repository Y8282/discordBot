import discord
from discord.ext import commands
from discord import app_commands
import random
from collections import defaultdict
import re
import time
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


user_count = defaultdict(lambda: {"count": 0, "time": 0})
# Client 실행법
# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f"로그인 완료! : {self.user} (ID: {self.user.id})")
#         print("------")
#         await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

guild_id = 1450068908764565569;

guild = discord.Object(id=guild_id)

# intents => 수신할수 있는 이벤트 유형을 결정해줌 -> all() 일경우 모든 유형의 이벤트 수신
intents = discord.Intents.all() 
intents.message_content = True
# Client => 상호작용 관리하는 부분
# client = MyClient(intents=intents)
#bot 실행법
bot = commands.Bot(command_prefix="!", intents=intents)

# tree => / 명령어 관리
#tree = app_commands.CommandTree(bot)

# bot 이 tree 관리중
tree = bot.tree

#yt-dlp 설정 => 유튜브에서 노래를 다운받는 라이브러리
# ytdl = yt_dlp.YoutubeDL({
#     'format': 'bestaudio',
#     'noplaylist': True,
# })

ffmpeg_options = {
    'options': '-vn',
}

@bot.event
async def on_ready():
    
    await tree.sync(guild=guild)
    print(f"로그인 완료! : {bot.user} (ID: {bot.user.id})")
    print("------")

# @bot.command()
# async def 안녕(ctx):
#     await ctx.send("안녕하세요! 명령어로 인사하기")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # if "안녕" in message.content:
    if re.match(r"(안녕|하이|헬로)", message.content):
        await message.channel.send("안녕하세요!")
    await bot.process_commands(message)


@tree.command(name="음식", description="음식 추천", guild=guild)
async def food_command(interaction: discord.Interaction):
    await recommend_food(interaction)


@tree.command(name="장소", description="장소 추천", guild=guild)
@app_commands.describe(option="지역 선택 (서울, 경기, 인천, 부산, 대구, 대전, 광주, 울산, 기타) 안쓰면 랜덤")
async def location_command(interaction: discord.Interaction, option: Optional[str]= None):
    await recommend_location(interaction, option)

@tree.command(name="도박", description="도박 게임", guild=guild)
@app_commands.describe(option="돈")
async def gambling_command(interaction: discord.Interaction, money: int):
    await gambling(interaction, money)

async def recommend_food(interaction: discord.Interaction):
    RESET_TIME = 3 * 60 * 60 # 3시간
    user_id = interaction.user.id
    now = time.time()

    if now - user_count[user_id]["time"] > RESET_TIME: # 3시간이 지났는지 확인
        user_count[user_id] = {"count": 0 , "time": now} # 카운트 초기화 및 시간 업데이트

    user_count[user_id]["count"] += 1
    user_count[user_id]["time"] = now
    
    menu = [
    "피자","치킨","햄버거","초밥","라면","김밥","떡볶이","순대","우동","짜장면",
    "짬뽕","탕수육","돈까스","제육볶음","불고기","삼겹살","갈비","냉면","비빔냉면","물냉면",
    "칼국수","수제비","감자탕","해장국","설렁탕","곰탕","육개장","닭갈비","찜닭","닭도리탕",
    "카레","오므라이스","볶음밥","계란찜","계란말이","샌드위치","토스트","핫도그","파스타","스테이크",
    "리조또","마라탕","마라샹궈","양꼬치","훠궈","케밥","타코","부리또","나초","팟타이",
    "쌀국수","분짜","반미","샤브샤브","월남쌈","김치찌개","된장찌개","부대찌개","순두부찌개","청국장",
    "비빔밥","돌솥비빔밥","알밥","유부초밥","장어덮밥","규동","가츠동","텐동","연어덮밥","참치덮밥",
    "토마토스파게티","크림파스타","로제파스타","봉골레","알리오올리오","라자냐","피쉬앤칩스","치즈볼","감자튀김","어니언링",
    "와플","팬케이크","프렌치토스트","아이스크림","빙수","마카롱","케이크","초콜릿","쿠키","도넛"
    ]
    answer = [
    "걍 알아서 찾아라",
    "적당히 물어봐라",
    "그냥 먹고싶은거 먹어라",
    "답정너 면서 왜 물어봄",
    "Fuck you",

    "또 물어보네 ㅋㅋ",
    "입은 왜 달고 다니냐",
    "눈에 보이는 거 먹어라",
    "그만 좀 고민해라",
    "그 정도면 아무거나 먹어도 맛있다",

    "지금 배고픈거지 메뉴가 문제가 아님",
    "그냥 배달앱 켜라",
    "냉장고부터 열어봐라",
    "이미 답 정해놓고 물어보지마라",
    "선택장애 왔냐",

    "이쯤되면 굶는게 답이다",
    "또 시키는거 시켜라 그냥",
    "먹고 싶은거 이미 떠올랐잖아",
    "시간 낭비하지 말고 먹어라",
    "그냥 치킨 시켜라 끝",

    "고민할 시간에 주문 가능",
    "너 지금 선택 미루는 중이다",
    "결정 못하면 아무거나 먹는게 답",
    "메뉴보다 니가 문제임",
    "그만 물어봐라 진짜",

    "밥 먹을 때까지 계속 물어볼거냐",
    "이 정도면 내가 골라줘도 불만이다",
    "결정 못하면 추천 의미 없다",
    "그냥 첫번째 생각난 거 먹어라",
    "먹는 것도 고민이면 답 없다"
]
    recommended = random.choice(menu)
    answerChoice = random.choice(answer)

    count = user_count[user_id]["count"]
    if count >= 10:
        await interaction.response.send_message("말 걸지마")
        return;
    if count >= 5:
        await interaction.response.send_message(f"{answerChoice}")
        return 
    if count >= 3:
        await interaction.response.send_message(f"'{recommended}'(이)나 먹자")
        return 
    if user_id == 813333804252266516:
        await interaction.response.send_message("넌 다이어트 해야겠지?")
        return
    await interaction.response.send_message(f"오늘의 추천 메뉴는 '{recommended}'입니다.")
    return

async def recommend_location(interaction: discord.Interaction , option: Optional[str]= None):

    locations = [
        # 서울
        "서울 강남","서울 홍대","서울 신촌","서울 이태원","서울 잠실",
        "서울 건대","서울 성수","서울 압구정","서울 청담","서울 종로",
        "서울 신림","서울 사당",
        "서울 명동","서울 을지로","서울 한남동","서울 북촌","서울 삼청동",

        # 경기
        "수원 인계동","수원 행궁동","성남 판교","성남 분당","고양 일산",
        "용인 기흥","안양 범계","부천 상동","의정부 민락동","남양주 다산",

        # 인천
        "인천 구월동","인천 송도","인천 부평","인천 청라","인천 월미도",

        # 부산
        "부산 해운대","부산 광안리","부산 서면","부산 남포동","부산 송정",

        # 대구
        "대구 동성로","대구 수성못","대구 앞산","대구 범어동",

        # 대전
        "대전 둔산동","대전 은행동","대전 유성","대전 관저동",

        # 광주
        "광주 상무지구","광주 충장로","광주 수완지구",

        # 울산
        "울산 삼산동","울산 성남동",

        # 기타
        "제주 애월","제주 협재","제주 성산일출봉","강릉 경포대","강릉 안목해변",
        "전주 한옥마을","여수 밤바다","춘천 닭갈비골목","속초 중앙시장"
        ]
    
    activities = [
    "볼링","보드게임카페",
    "PC방","노래방","방탈출",
    "술집이나","게임센터","당구장",
    "강범진 집 털기", "흐에집들이", 
    "실내사격장" , "실내스크린야구장"
    ]

    options = ["서울", "경기", "인천", "부산", "대구", "대전", "광주", "울산", "기타"]
    if option and option not in options:
        await interaction.response.send_message("올바른 옵션을 선택해주세요. (서울, 경기, 인천, 부산, 대구, 대전, 광주, 울산, 기타)")
        return
    if option:
        if option == "서울":
            locations = [loc for loc in locations if loc.startswith("서울")]
        elif option == "경기":
            locations = [loc for loc in locations if loc.startswith("수원") or loc.startswith("성남") or loc.startswith("고양") or loc.startswith("용인") or loc.startswith("안양") or loc.startswith("부천") or loc.startswith("의정부") or loc.startswith("남양주")]
        elif option == "인천":
            locations = [loc for loc in locations if loc.startswith("인천")]
        elif option == "부산":
            locations = [loc for loc in locations if loc.startswith("부산")]
        elif option == "대구":
            locations = [loc for loc in locations if loc.startswith("대구")]
        elif option == "대전":
            locations = [loc for loc in locations if loc.startswith("대전")]
        elif option == "광주":
            locations = [loc for loc in locations if loc.startswith("광주")]
        elif option == "울산":
            locations = [loc for loc in locations if loc.startswith("울산")]
        elif option == "기타":
            locations = [loc for loc in locations if loc.startswith("제주") or loc.startswith("강릉") or loc.startswith("전주") or loc.startswith("여수") or loc.startswith("춘천") or loc.startswith("속초")]
        
    place = random.choice(locations)
    activity = random.choice(activities)

    await interaction.response.send_message(  f"{place} 에서 {activity} 가라")




bot.run(TOKEN)