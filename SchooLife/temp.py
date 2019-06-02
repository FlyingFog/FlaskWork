for i in range(10):
    print("u{} = models.User(email=\"u{}@qq.com\", username='u{}',password=models.generate_password_hash(\"123\"), confirmed=1)".format(i,i,i))