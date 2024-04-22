from config import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email_id', 'address', 'add_on')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class WallSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'admin', 'title', 'description', 'add_on')


wall_schema = WallSchema()
walls_schema = WallSchema(many=True)
