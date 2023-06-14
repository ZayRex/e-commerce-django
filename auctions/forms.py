from django import forms
from .models import AuctionListing

class ListingForm(forms.ModelForm):

    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'current_price', 'image_url', 'category']

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)