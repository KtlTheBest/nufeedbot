import sqlite3

class DBHandler():
	def __init__(self):
		self.id_database_name = "user_ids.db"
		self.id_conn = sqlite3.connect(self.id_database_name)
		self.post_database_name = "latest_post.db"
		self.post_conn = sqlite3.connect(self.post_database_name)

	def setup(self):
		statement = "CREATE TABLE IF NOT EXISTS user_ids (id int)"
		self.id_conn.execute(statement)
		self.id_conn.commit()

	def add_id(self, id_to_add):
		statement = "INSERT INTO user_ids (id) VALUES (?)"
		args = (id_to_add, )
		self.id_conn.execute(statement, args)
		self.id_conn.commit()

	def delete_item(self, id_to_del):
		statement = "DELETE FROM user_ids WHERE id = (?)"
		args = (id_to_del, )
		self.id_conn.execute(statement, args)
		self.id_conn.commit()

	def get_items(self):
		statement = "SELECT id FROM user_ids"
		return [x[0] for x in self.id_conn.execute(statement)]

	def setup_latest_post(self):
		statement = "CREATE TABLE IF NOT EXISTS post (latest text)"
		self.post_conn.execute(statement)

	def add_latest_post(self, post):
		statement = "INSERT INTO post (latest) VALUES (?)"
		args = (post, )
		self.post_conn.execute(statement, args)
		self.post_conn.commit()

	def delete_latest_post(self, post):
		statement = "DELETE FROM post WHERE latest = (?)"
		args = (post, )
		self.post_conn.execute(statement, args)
		self.post_conn.commit()

	def get_latest_post(self):
		statement = "SELECT latest FROM post"
		return [x[0] for x in self.post_conn.execute(statement)]

	def update_latest_post(self, old, new):
		if old != "":
			self.delete_latest_post(old)
		self.add_latest_post(new)
