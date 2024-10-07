from django.contrib import admin

from .models import Conversation, Message
# Register your models here.

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [MessageInline]

admin.site.register(Conversation, ConversationAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'sent_to']
admin.site.register(Message, MessageAdmin)