from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


# サンプルユーザー作成
def sample_user(email='test@example.com', password='test123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    # ユーザーのメアドとパスワードチェック
    def test_create_user_save_email_and_password(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # メアドが小文字になるか
    def test_create_user_normalize_email(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    # メアドがないときエラーになるか
    def test_create_user_not_email_raise(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    # adminユーザーが作成できるか
    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # タグがstringかつ存在するかどうか
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Tag name is Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    # ingredientが生成できるか
    def test_ingredient_str(self):
        """Test the ingredient string respresentation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    # recipeが生成できるか
    def test_recipe_str(self):
        """Test the recipe string respresentation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    # imageをパス通りに保存できるか
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-id'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
