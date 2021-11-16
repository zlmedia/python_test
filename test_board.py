import sqlite3  # 설치 필요없음.

dbpath = "board.sqlite"
conn = sqlite3.connect(dbpath)

class boardClass:
	def __init__(self):
		self.db_init()

	def db_init(self):
		# DB 테이블 만들기
		cur = conn.cursor()
		# cur.execute("DROP TABLE IF EXISTS free")       # 기존에 items 테이블이 있다면 지우기
		cur.execute("""
				CREATE TABLE IF NOT EXISTS free (
				num         INTEGER PRIMARY KEY,
				title       TEXT,
				writer      TEXT,
				contents    TEXT)
				""")
		conn.commit()

	def board_list(self):
		cur = conn.cursor()
		cur.execute("SELECT * FROM free")
		fr_list = cur.fetchall()
		print(f"=" * 80)
		print(f"{'no': ^4}{'제목': ^56}{'글쓴이': <10}")
		print(f"=" * 80)
		for fr in fr_list:
			content_len = len(fr[1])
			print(f"{fr[0]: ^4}{fr[1]: <56}{fr[2]: <10}")
		print(f"=" * 80)

	def board_write(self):
		title = input("제목 : ")
		writer = input("글쓴이 : ")
		contents = input("내용 : ")

		cur = conn.cursor()
		data = [(title, writer, contents)]
		cur.executemany("INSERT INTO free(title, writer, contents) VALUES(?,?,?)", data)
		conn.commit()
		
	def board_view(self, num):
		cur = conn.cursor()
		data = [num]

		try:
			cur.execute("SELECT * FROM free WHERE num=?", data)
			(no, title, writer, contents) = cur.fetchone()
		except:
			print(" num error")
			return

		print(f"no:{no}\n제목:{title}\n글쓴이:{writer}")
		print(f"내용:{contents}")

# ===============================================================================================
if __name__ == "__main__":
    board = boardClass()
    board.db_init()

    while True:
        print('')
        board.board_list()
        cmd = input(f"X:Quit W:글쓰기 번호:글내용보기 > ").strip()
        cmd_up = cmd.upper()

        if cmd == '':
            continue
        # Quit
        elif cmd_up == 'X' or cmd_up == 'Q':
            print(' -----> Good Bye... ^^')
            break
        # write
        elif cmd_up == 'W':
            board.board_write()
        # 글내요 보기
        elif cmd.isdecimal():
            board.board_view(int(cmd))
        else:
            break
