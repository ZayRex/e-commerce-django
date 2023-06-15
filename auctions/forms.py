from django import forms
from .models import AuctionListing, Comment

class ListingForm(forms.ModelForm):

    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'current_price', 'image_url', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']