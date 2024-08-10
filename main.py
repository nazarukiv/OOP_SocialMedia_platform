from typing import List, Optional

# User Class
class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password
        self.friends = []
        self.posts = []
        self.messages = []
        self.profile_picture = None
        self.bio = ""
        self.status = "Active"
        self.privacy_settings = {"posts": "public", "messages": "friends_only"}
        self.activity_log = []

    def update_profile(self, profile_picture: Optional[str] = None, bio: Optional[str] = None,
                       status: Optional[str] = None):
        if profile_picture:
            self.profile_picture = profile_picture
        if bio:
            self.bio = bio
        if status:
            self.status = status

    def set_privacy(self, posts: Optional[str] = None, messages: Optional[str] = None):
        if posts:
            self.privacy_settings["posts"] = posts
        if messages:
            self.privacy_settings["messages"] = messages

    def log_activity(self, activity: str):
        self.activity_log.append(activity)

    def add_friend(self, user: 'User'):
        if user not in self.friends:
            self.friends.append(user)
            self.log_activity(f"Added {user.username} as a friend")

    def remove_friend(self, user: 'User'):
        if user in self.friends:
            self.friends.remove(user)
            self.log_activity(f"Removed {user.username} from friends")

    def send_message(self, recipient: 'User', content: str, attachments: Optional[List[str]] = None):
        message = Message(self, recipient, content, attachments)
        self.messages.append(message)
        recipient.messages.append(message)
        self.log_activity(f"Sent a message to {recipient.username}")
        return message

    def create_post(self, content: str, visibility: str = "public"):
        post = Post(self, content, visibility)
        self.posts.append(post)
        self.log_activity(f"Created a post: {post.display_post()}")
        return post

    def __str__(self):
        return f"User: {self.username}\nEmail: {self.email}\nBio: {self.bio}\nStatus: {self.status}\n"


# Post Class
class Post:
    def __init__(self, author: User, content: str, visibility: str = "public"):
        self.author = author
        self.content = content
        self.likes = set()
        self.comments = []
        self.visibility = visibility

    def like(self, user: User):
        self.likes.add(user)
        user.log_activity(f"Liked a post by {self.author.username}")

    def add_comment(self, author: User, content: str):
        comment = Comment(author, content)
        self.comments.append(comment)
        author.log_activity(f"Commented on a post by {self.author.username}")

    def edit_post(self, new_content: str):
        self.content = new_content

    def share_post(self, user: User):
        user.log_activity(f"Shared a post by {self.author.username}")

    def display_post(self):
        return f"Post by {self.author.username}: {self.content}\nLikes: {len(self.likes)}\nComments: {[c.display_comment() for c in self.comments]}"


# Comment Class
class Comment:
    def __init__(self, author: User, content: str):
        self.author = author
        self.content = content

    def display_comment(self):
        return f"{self.author.username}: {self.content}"


# Message Class
class Message:
    def __init__(self, sender: User, receiver: User, content: str, attachments: Optional[List[str]] = None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.attachments = attachments if attachments else []
        self.read_status = False

    def mark_as_read(self):
        self.read_status = True

    def display_message(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content}\nAttachments: {self.attachments}\nRead: {self.read_status}"


# Notification Class
class Notification:
    def __init__(self, user: User, message: str):
        self.user = user
        self.message = message
        self.timestamp = "2024-08-01 12:00:00"
        self.read = False

    def mark_as_read(self):
        self.read = True

    def display_notification(self):
        return f"Notification for {self.user.username}: {self.message} at {self.timestamp}\nRead: {self.read}"


# Group Class
class Group:
    def __init__(self, name: str):
        self.name = name
        self.members = []
        self.posts = []

    def add_member(self, member: User):
        if member not in self.members:
            self.members.append(member)
            member.log_activity(f"Added to group {self.name}")

    def remove_member(self, member: User):
        if member in self.members:
            self.members.remove(member)
            member.log_activity(f"Removed from group {self.name}")

    def create_post(self, author: User, content: str):
        post = Post(author, content)
        self.posts.append(post)
        return post

    def display_group(self):
        return f"Group: {self.name}\nMembers: {[member.username for member in self.members]}"


# Event Class
class Event:
    def __init__(self, name: str, date: str, location: str, category: Optional[str] = None):
        self.name = name
        self.date = date
        self.location = location
        self.category = category
        self.participants = []

    def add_participant(self, user: User):
        if user not in self.participants:
            self.participants.append(user)
            user.log_activity(f"Joined event {self.name}")

    def remove_participant(self, user: User):
        if user in self.participants:
            self.participants.remove(user)
            user.log_activity(f"Left event {self.name}")

    def display_event(self):
        return f"Event: {self.name}\nDate: {self.date}\nLocation: {self.location}\nCategory: {self.category}\nParticipants: {[user.username for user in self.participants]}"


# Search Class
class Search:
    def __init__(self, query: str):
        self.query = query

    def search_users(self, users: List[User]):
        return [user for user in users if self.query.lower() in user.username.lower()]

    def search_posts(self, posts: List[Post]):
        return [post for post in posts if self.query.lower() in post.content.lower()]

    def search_groups(self, groups: List[Group]):
        return [group for group in groups if self.query.lower() in group.name.lower()]


# Recommendation Class
class Recommendation:
    def __init__(self, user: User):
        self.user = user
        self.recommendations = []

    def generate_recommendations(self):
        self.recommendations = [
            f"Recommend new friends based on {self.user.username}'s activity.",
            f"Recommend posts similar to {self.user.username}'s interests."
        ]
        return self.recommendations


# Message Thread Class
class MessageThread:
    def __init__(self, participants: List[User]):
        self.participants = participants
        self.messages = []

    def add_message(self, message: Message):
        if message.sender in self.participants and message.receiver in self.participants:
            self.messages.append(message)

    def display_thread(self):
        return [msg.display_message() for msg in self.messages]


# Activity Feed Class
class ActivityFeed:
    def __init__(self, user: User):
        self.user = user

    def display_feed(self):
        feed = []
        for post in self.user.posts:
            feed.append(post.display_post())
        for message in self.user.messages:
            feed.append(message.display_message())
        return feed


# User Report Class
class UserReport:
    def __init__(self, user: User):
        self.user = user

    def generate_report(self):
        return {
            "username": self.user.username,
            "email": self.user.email,
            "bio": self.user.bio,
            "posts_count": len(self.user.posts),
            "messages_count": len(self.user.messages),
            "friends_count": len(self.user.friends),
            "activity_log": self.user.activity_log
        }


# Additional Utility Functions
def simulate_user_activity(user: User, post_content: str, message_content: str, recipient: User):
    post = user.create_post(post_content)
    print(f"User {user.username} created a post: {post.display_post()}")
    message = user.send_message(recipient, message_content)
    print(f"User {user.username} sent a message: {message.display_message()}")


def simulate_notifications(users: List[User]):
    for user in users:
        notification = Notification(user, "You have a new message or activity.")
        print(notification.display_notification())


def create_large_data_set():
    users = []
    for i in range(100):
        username = f"user{i}"
        email = f"user{i}@example.com"
        password = f"password{i}"
        user = User(username, email, password)
        users.append(user)

    posts = []
    for user in users:
        for j in range(5):
            post = user.create_post(f"Post {j} by {user.username}")
            posts.append(post)

    return users, posts


def main():
    alice = User("Alice", "alice@example.com", "password123")
    bob = User("Bob", "bob@example.com", "password456")
    charlie = User("Charlie", "charlie@example.com", "password789")

    alice.add_friend(bob)
    bob.add_friend(charlie)

    post1 = alice.create_post("Hello, world!")
    post2 = bob.create_post("Good morning!")

    alice.create_post("Hello, world!").like(bob)  # Alice likes Bob's post
    alice.create_post("Hello, world!").add_comment(alice, "Nice post!")

    message = alice.send_message(bob, "How are you?")

    # Create Group and Event
    group = Group("Developers")
    group.add_member(alice)
    group.add_member(bob)
    group.create_post(alice, "Join us for a coding event!")

    event = Event("Coding Workshop", "2024-08-15", "New York")
    event.add_participant(alice)
    event.add_participant(bob)

    # Search
    search = Search("alice")
    print(search.search_users([alice, bob, charlie]))

    recommendation = Recommendation(alice)
    print(recommendation.generate_recommendations())


    thread = MessageThread([alice, bob])
    thread.add_message(message)
    print(thread.display_thread())


    feed = ActivityFeed(alice)
    print(feed.display_feed())


    report = UserReport(alice)
    print(report.generate_report())

    simulate_user_activity(alice, "Check out this cool post!", "What’s up, Bob?", bob)

    simulate_notifications([alice, bob, charlie])

if __name__ == "__main__":
    main()
