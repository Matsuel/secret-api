Table users {
  id integer [primary key]
  username varchar
  password varchar
  followsCount integer
  followersCount integer
}

Table followers {
  id integer [primary key]
  user_id integer
  follower_id integer
}

Table secrets {
  id integer [primary key]
  text varchar
  user_id integer
  category_id integer
  is_public bool
  shared_space_id integer
  anonymous bool
  likesCount integer
}

Table categories {
  id integer [primary key]
  name varchar
}

Table liked_secrets {
  id integer [primary key]
  secret_id integer
  user_id integer
}

Table shared_spaces_users {
  id integer [primary key]
  user_id integer
  shared_space_id integer
  invitation_accepted bool
}

Table shared_spaces {
  id integer [primary key]
  name varchar
  is_public bool
}

Ref: liked_secrets.user_id > users.id
Ref: shared_spaces_users.user_id > users.id
Ref: secrets.user_id > users.id
Ref: followers.user_id > users.id
Ref: followers.follower_id > users.id
Ref: shared_spaces_users.shared_space_id > shared_spaces.id
Ref: secrets.shared_space_id > shared_spaces.id
Ref: secrets.category_id > categories.id
Ref: liked_secrets.secret_id > secrets.id