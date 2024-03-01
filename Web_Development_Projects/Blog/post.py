import requests

class Post:
    """
    A class representing a blog post.

    Attributes:
        id (int): The post's unique identifier.
        title (str): The title of the post.
        subtitle (str): The subtitle of the post.
        body (str): The main content body of the post.
    """

    def __init__(self, post_id, title, subtitle, author, image, body):
        """
        Initializes a new instance of the Post class.

        Args:
            post_id (int): The unique identifier for the post.
            title (str): The title of the post.
            subtitle (str): The subtitle of the post.
            author (str): The author of the post.
            image (str): The name of the image to display with the post.
            body (str): The main content of the post.
        """
        self.id = post_id
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.image = image
        self.body = body

    def __repr__(self):
        """Provides an unambiguous representation of the object."""
        return f'<Post {self.id}: {self.title}>'

    def __str__(self):
        """Provides a readable representation of the object."""
        return f'{self.title} - {self.subtitle}'

    @classmethod
    def all_posts(cls, url="https://api.npoint.io/1be06ecaaa3d4d3eabc1"):
        """
        Fetches all posts from a given URL and returns them as Post instances.

        Args:
            url (str): The URL to fetch the posts from. Defaults to a predefined URL.

        Returns:
            list[Post]: A list of Post instances created from the fetched post data.

        Raises:
            requests.HTTPError: If the request to the API fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # This will raise an HTTPError if the request returned an unsuccessful status code.
        except requests.RequestException as e:
            print(f"Failed to fetch posts: {e}")
            return []

        all_posts = response.json()
        return [cls(post['id'], post['title'], post['subtitle'], post['author'], post['image'], post['body']) for post in all_posts]

# Example usage:
if __name__ == "__main__":
    posts = Post.all_posts()
    for post in posts:
        print(post)
