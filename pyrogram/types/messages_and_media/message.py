#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations
import logging
import asyncio
from datetime import datetime
from functools import partial
from typing import List, Match, Union, BinaryIO, Optional, Callable, Dict, Any, cast

import pyrogram
from pyrogram import raw, enums, utils
from pyrogram import filters
from pyrogram.types.pyromod import ListenerTypes
from pyrogram.errors import MessageIdsEmpty, PeerIdInvalid, ChannelPrivate, FloodWait, FloodPremiumWait
from pyrogram.parser import utils as parser_utils, Parser
from ..object import Object
from ..update import Update

import pyrogram.types as pyrogram_types
import pyrogram.raw.types as raw_types
import pyrogram.raw.functions as raw_functions
import pyrogram.raw.base as raw_base

log = logging.getLogger(__name__)


class Str(str):
    def __init__(self, *args: Any):
        super().__init__()
        self.entities: Optional[List[pyrogram_types.MessageEntity]] = None

    def init(self, entities: Optional[List[pyrogram_types.MessageEntity]]) -> Str:
        self.entities = entities
        return self

    @property
    def markdown(self) -> str:
        return Parser.unparse(self, self.entities or [], False)

    @property
    def html(self) -> str:
        return Parser.unparse(self, self.entities or [], True)

    def __getitem__(self, item: Any) -> str:
        return parser_utils.remove_surrogates(parser_utils.add_surrogates(self)[item])


class Message(Object, Update):
    topic: Optional[pyrogram_types.ForumTopic] = None
    reply_to_story_chat_id: Optional[int] = None
    quote: Optional[pyrogram_types.TextQuote] = None
    reply_to_message_id: Optional[int] = None
    reply_to_top_message_id: Optional[int] = None
    reply_to_story_id: Optional[int] = None
    reply_to_story_user_id: Optional[int] = None
    reply_to_message: Optional[Message] = None
    reply_to_story: Optional[pyrogram_types.Story] = None

    def __init__(
        self,
        *,
        client: Optional[pyrogram.Client] = None,
        id: Optional[int] = None,
        from_user: Optional[pyrogram_types.User] = None,
        sender_chat: Optional[pyrogram_types.Chat] = None,
        date: Optional[datetime] = None,
        chat: Optional[pyrogram_types.Chat] = None,
        topics: Optional[pyrogram_types.ForumTopic] = None,
        forward_from: Optional[pyrogram_types.User] = None,
        forward_sender_name: Optional[str] = None,
        forward_from_chat: Optional[pyrogram_types.Chat] = None,
        forward_from_message_id: Optional[int] = None,
        forward_signature: Optional[str] = None,
        forward_date: Optional[datetime] = None,
        is_topic_message: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        reply_to_story_id: Optional[int] = None,
        reply_to_story_user_id: Optional[int] = None,
        reply_to_top_message_id: Optional[int] = None,
        reply_to_message: Optional[Message] = None,
        reply_to_story: Optional[pyrogram_types.Story] = None,
        mentioned: Optional[bool] = None,
        empty: Optional[bool] = None,
        service: Optional[enums.MessageServiceType] = None,
        scheduled: Optional[bool] = None,
        from_scheduled: Optional[bool] = None,
        edit_hide: Optional[bool] = None,
        media: Optional[enums.MessageMediaType] = None,
        invert_media: Optional[bool] = None,
        edit_date: Optional[datetime] = None,
        media_group_id: Optional[str] = None,
        author_signature: Optional[str] = None,
        has_protected_content: Optional[bool] = None,
        has_media_spoiler: Optional[bool] = None,
        text: Optional[Str] = None,
        quote_text: Optional[Str] = None,
        entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        audio: Optional[pyrogram_types.Audio] = None,
        document: Optional[pyrogram_types.Document] = None,
        photo: Optional[pyrogram_types.Photo] = None,
        sticker: Optional[pyrogram_types.Sticker] = None,
        animation: Optional[pyrogram_types.Animation] = None,
        game: Optional[pyrogram_types.Game] = None,
        giveaway: Optional[pyrogram_types.Giveaway] = None,
        story: Optional[pyrogram_types.MessageStory] = None,
        video: Optional[pyrogram_types.Video] = None,
        voice: Optional[pyrogram_types.Voice] = None,
        video_note: Optional[pyrogram_types.VideoNote] = None,
        caption: Optional[Str] = None,
        contact: Optional[pyrogram_types.Contact] = None,
        location: Optional[pyrogram_types.Location] = None,
        venue: Optional[pyrogram_types.Venue] = None,
        web_page: Optional[pyrogram_types.WebPage] = None,
        poll: Optional[pyrogram_types.Poll] = None,
        dice: Optional[pyrogram_types.Dice] = None,
        new_chat_members: Optional[List[pyrogram_types.User]] = None,
        left_chat_member: Optional[pyrogram_types.User] = None,
        new_chat_title: Optional[str] = None,
        new_chat_photo: Optional[pyrogram_types.Photo] = None,
        delete_chat_photo: Optional[bool] = None,
        group_chat_created: Optional[bool] = None,
        supergroup_chat_created: Optional[bool] = None,
        channel_chat_created: Optional[bool] = None,
        migrate_to_chat_id: Optional[int] = None,
        migrate_from_chat_id: Optional[int] = None,
        pinned_message: Optional[Message] = None,
        game_high_score: Optional[int] = None,
        views: Optional[int] = None,
        forwards: Optional[int] = None,
        via_bot: Optional[pyrogram_types.User] = None,
        outgoing: Optional[bool] = None,
        quote: Optional[pyrogram_types.TextQuote] = None,
        matches: Optional[List[Match[Any]]] = None,
        command: Optional[List[str]] = None,
        forum_topic_created: Optional[pyrogram_types.ForumTopicCreated] = None,
        forum_topic_closed: Optional[pyrogram_types.ForumTopicClosed] = None,
        forum_topic_reopened: Optional[pyrogram_types.ForumTopicReopened] = None,
        forum_topic_edited: Optional[pyrogram_types.ForumTopicEdited] = None,
        general_topic_hidden: Optional[pyrogram_types.GeneralTopicHidden] = None,
        general_topic_unhidden: Optional[pyrogram_types.GeneralTopicUnhidden] = None,
        video_chat_scheduled: Optional[pyrogram_types.VideoChatScheduled] = None,
        video_chat_started: Optional[pyrogram_types.VideoChatStarted] = None,
        video_chat_ended: Optional[pyrogram_types.VideoChatEnded] = None,
        video_chat_members_invited: Optional[pyrogram_types.VideoChatMembersInvited] = None,
        web_app_data: Optional[pyrogram_types.WebAppData] = None,
        giveaway_launched: Optional[bool] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        reactions: Optional[List[pyrogram_types.Reaction]] = None
    ):
        super().__init__(client)
        self.id = id or 0
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.chat = chat
        self.topics = topics
        self.forward_from = forward_from
        self.forward_sender_name = forward_sender_name
        self.forward_from_chat = forward_from_chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_date = forward_date
        self.is_topic_message = is_topic_message
        self.message_thread_id = message_thread_id
        self.effect_id = effect_id
        self.reply_to_message_id = reply_to_message_id
        self.reply_to_story_id = reply_to_story_id
        self.reply_to_story_user_id = reply_to_story_user_id
        self.reply_to_top_message_id = reply_to_top_message_id
        self.reply_to_message = reply_to_message
        self.reply_to_story = reply_to_story
        self.mentioned = mentioned
        self.empty = empty
        self.service = service
        self.scheduled = scheduled
        self.from_scheduled = from_scheduled
        self.media = media
        self.invert_media = invert_media
        self.edit_date = edit_date
        self.edit_hide = edit_hide
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.has_protected_content = has_protected_content
        self.has_media_spoiler = has_media_spoiler
        self.text = text
        self.quote_text = quote_text
        self.entities = entities
        self.caption_entities = caption_entities
        self.quote_entities = quote_entities
        self.audio = audio
        self.document = document
        self.photo = photo
        self.sticker = sticker
        self.animation = animation
        self.game = game
        self.giveaway = giveaway
        self.story = story
        self.video = video
        self.voice = voice
        self.video_note = video_note
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.web_page = web_page
        self.poll = poll
        self.dice = dice
        self.new_chat_members = new_chat_members
        self.left_chat_member = left_chat_member
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = pinned_message
        self.game_high_score = game_high_score
        self.views = views
        self.forwards = forwards
        self.via_bot = via_bot
        self.outgoing = outgoing
        self.quote = quote
        self.matches = matches
        self.command = command
        self.reply_markup = reply_markup
        self.forum_topic_created = forum_topic_created
        self.forum_topic_closed = forum_topic_closed
        self.forum_topic_reopened = forum_topic_reopened
        self.forum_topic_edited = forum_topic_edited
        self.general_topic_hidden = general_topic_hidden
        self.general_topic_unhidden = general_topic_unhidden
        self.video_chat_scheduled = video_chat_scheduled
        self.video_chat_started = video_chat_started
        self.video_chat_ended = video_chat_ended
        self.video_chat_members_invited = video_chat_members_invited
        self.web_app_data = web_app_data
        self.giveaway_launched = giveaway_launched
        self.reactions = reactions

    async def wait_for_click(
        self,
        from_user_id: Union[int, str, List[Union[int, str]], None] = None,
        timeout: Optional[int] = None,
        filters: Any = None,
        alert: Union[str, bool] = True,
    ) -> pyrogram_types.CallbackQuery:
        message_id = getattr(self, "id", getattr(self, "message_id", None))
        result = await self._client.listen(
            listener_type=pyrogram_types.ListenerTypes.CALLBACK_QUERY,
            timeout=timeout,
            filters=filters,
            unallowed_click_alert=alert,
            chat_id=self.chat.id if self.chat else None,
            user_id=from_user_id,
            message_id=message_id,
        )
        return cast(pyrogram_types.CallbackQuery, result)

    @staticmethod
    async def _parse(
        client: pyrogram.Client,
        message: raw_base.Message,
        users: dict[int, Any],
        chats: dict[int, Any],
        topics: Optional[dict[int, Any]] = None,
        is_scheduled: bool = False,
        replies: int = 1
    ) -> Optional[Message]:
        if isinstance(message, raw_types.MessageEmpty):
            return Message(id=message.id, empty=True, client=client)

        from_id = utils.get_raw_peer_id(message.from_id)
        peer_id = utils.get_raw_peer_id(message.peer_id)
        user_id = from_id or peer_id

        if isinstance(message.from_id, raw_types.PeerUser) and isinstance(message.peer_id, raw_types.PeerUser):
            if from_id not in users or peer_id not in users:
                try:
                    if from_id is not None and peer_id is not None:
                        r = await client.invoke(
                            raw_functions.users.GetUsers(
                                id=[
                                    await client.resolve_peer(from_id),
                                    await client.resolve_peer(peer_id)
                                ]
                            )
                        )
                        users.update({i.id: i for i in r})
                except PeerIdInvalid:
                    pass

        if isinstance(message, raw_types.MessageService):
            message_thread_id = None
            action = message.action

            new_chat_members = None
            left_chat_member = None
            new_chat_title = None
            delete_chat_photo = None
            migrate_to_chat_id = None
            migrate_from_chat_id = None
            group_chat_created = None
            channel_chat_created = None
            new_chat_photo = None
            is_topic_message = None
            forum_topic_created = None
            forum_topic_closed = None
            forum_topic_reopened = None
            forum_topic_edited = None
            general_topic_hidden = None
            general_topic_unhidden = None
            video_chat_scheduled = None
            video_chat_started = None
            video_chat_ended = None
            video_chat_members_invited = None
            web_app_data = None
            giveaway_launched = None
            service_type = None

            if isinstance(action, raw_types.MessageActionChatAddUser):
                new_chat_members = [pyrogram_types.User._parse(client, users[i]) for i in action.users if i in users]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
            elif isinstance(action, raw_types.MessageActionChatJoinedByLink):
                raw_peer = utils.get_raw_peer_id(message.from_id)
                if raw_peer in users:
                    new_chat_members = [pyrogram_types.User._parse(client, users[raw_peer])]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
            elif isinstance(action, raw_types.MessageActionChatDeleteUser):
                if action.user_id in users:
                    left_chat_member = pyrogram_types.User._parse(client, users[action.user_id])
                service_type = enums.MessageServiceType.LEFT_CHAT_MEMBERS
            elif isinstance(action, raw_types.MessageActionChatEditTitle):
                new_chat_title = action.title
                service_type = enums.MessageServiceType.NEW_CHAT_TITLE
            elif isinstance(action, raw_types.MessageActionChatDeletePhoto):
                delete_chat_photo = True
                service_type = enums.MessageServiceType.DELETE_CHAT_PHOTO
            elif isinstance(action, raw_types.MessageActionChatMigrateTo):
                migrate_to_chat_id = action.channel_id
                service_type = enums.MessageServiceType.MIGRATE_TO_CHAT_ID
            elif isinstance(action, raw_types.MessageActionChannelMigrateFrom):
                migrate_from_chat_id = action.chat_id
                service_type = enums.MessageServiceType.MIGRATE_FROM_CHAT_ID
            elif isinstance(action, raw_types.MessageActionChatCreate):
                group_chat_created = True
                service_type = enums.MessageServiceType.GROUP_CHAT_CREATED
            elif isinstance(action, raw_types.MessageActionChannelCreate):
                channel_chat_created = True
                service_type = enums.MessageServiceType.CHANNEL_CHAT_CREATED
            elif isinstance(action, raw_types.MessageActionChatEditPhoto):
                new_chat_photo = pyrogram_types.Photo._parse(client, action.photo)
                service_type = enums.MessageServiceType.NEW_CHAT_PHOTO
            elif isinstance(action, raw_types.MessageActionTopicCreate):
                forum_topic_created = pyrogram_types.ForumTopicCreated._parse(message)
                service_type = enums.MessageServiceType.FORUM_TOPIC_CREATED
            elif isinstance(action, raw_types.MessageActionTopicEdit):
                if action.title:
                    forum_topic_edited = pyrogram_types.ForumTopicEdited._parse(action)
                    service_type = enums.MessageServiceType.FORUM_TOPIC_EDITED
                elif action.hidden:
                    general_topic_hidden = pyrogram_types.GeneralTopicHidden()
                    service_type = enums.MessageServiceType.GENERAL_TOPIC_HIDDEN
                elif action.closed:
                    forum_topic_closed = pyrogram_types.ForumTopicClosed()
                    service_type = enums.MessageServiceType.FORUM_TOPIC_CLOSED
                else:
                    if hasattr(action, "hidden") and action.hidden:
                        general_topic_unhidden = pyrogram_types.GeneralTopicUnhidden()
                        service_type = enums.MessageServiceType.GENERAL_TOPIC_UNHIDDEN
                    else:
                        forum_topic_reopened = pyrogram_types.ForumTopicReopened()
                        service_type = enums.MessageServiceType.FORUM_TOPIC_REOPENED
            elif isinstance(action, raw_types.MessageActionGroupCallScheduled):
                video_chat_scheduled = pyrogram_types.VideoChatScheduled._parse(action)
                service_type = enums.MessageServiceType.VIDEO_CHAT_SCHEDULED
            elif isinstance(action, raw_types.MessageActionGroupCall):
                if action.duration:
                    video_chat_ended = pyrogram_types.VideoChatEnded._parse(action)
                    service_type = enums.MessageServiceType.VIDEO_CHAT_ENDED
                else:
                    video_chat_started = pyrogram_types.VideoChatStarted()
                    service_type = enums.MessageServiceType.VIDEO_CHAT_STARTED
            elif isinstance(action, raw_types.MessageActionInviteToGroupCall):
                video_chat_members_invited = pyrogram_types.VideoChatMembersInvited._parse(client, action, users)
                service_type = enums.MessageServiceType.VIDEO_CHAT_MEMBERS_INVITED
            elif isinstance(action, raw_types.MessageActionWebViewDataSentMe):
                web_app_data = pyrogram_types.WebAppData._parse(action)
                service_type = enums.MessageServiceType.WEB_APP_DATA
            elif isinstance(action, raw_types.MessageActionGiveawayLaunch):
                giveaway_launched = True
                service_type = enums.MessageServiceType.GIVEAWAY_LAUNCHED

            from_user = pyrogram_types.User._parse(client, users.get(user_id, None))
            sender_chat = pyrogram_types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                date=utils.timestamp_to_datetime(message.date),
                chat=pyrogram_types.Chat._parse(client, message, users, chats, is_chat=True),
                topics=None,
                from_user=from_user,
                sender_chat=sender_chat,
                service=service_type,
                new_chat_members=new_chat_members,
                left_chat_member=left_chat_member,
                new_chat_title=new_chat_title,
                new_chat_photo=new_chat_photo,
                delete_chat_photo=delete_chat_photo,
                migrate_to_chat_id=utils.get_channel_id(migrate_to_chat_id) if migrate_to_chat_id else None,
                migrate_from_chat_id=-migrate_from_chat_id if migrate_from_chat_id else None,
                group_chat_created=group_chat_created,
                channel_chat_created=channel_chat_created,
                is_topic_message=is_topic_message,
                forum_topic_created=forum_topic_created,
                forum_topic_closed=forum_topic_closed,
                forum_topic_reopened=forum_topic_reopened,
                forum_topic_edited=forum_topic_edited,
                general_topic_hidden=general_topic_hidden,
                general_topic_unhidden=general_topic_unhidden,
                video_chat_scheduled=video_chat_scheduled,
                video_chat_started=video_chat_started,
                video_chat_ended=video_chat_ended,
                video_chat_members_invited=video_chat_members_invited,
                web_app_data=web_app_data,
                giveaway_launched=giveaway_launched,
                client=client
            )

            if isinstance(action, raw_types.MessageActionPinMessage):
                try:
                    if parsed_message.chat:
                        parsed_message.pinned_message = await client.get_messages(
                            parsed_message.chat.id,
                            reply_to_message_ids=message.id,
                            replies=0
                        )
                        parsed_message.service = enums.MessageServiceType.PINNED_MESSAGE
                except MessageIdsEmpty:
                    pass

            if isinstance(action, raw_types.MessageActionGameScore):
                parsed_message.game_high_score = pyrogram_types.GameHighScore._parse_action(client, message, users)
                if message.reply_to and replies and parsed_message.chat:
                    try:
                        parsed_message.reply_to_message = await client.get_messages(
                            parsed_message.chat.id,
                            reply_to_message_ids=message.id,
                            replies=0
                        )
                        parsed_message.service = enums.MessageServiceType.GAME_HIGH_SCORE
                    except MessageIdsEmpty:
                        pass

            if parsed_message.chat is not None:
                client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            if message.reply_to:
                if message.reply_to.forum_topic:
                    if message.reply_to.reply_to_top_id:
                        parsed_message.message_thread_id = message.reply_to.reply_to_top_id
                    else:
                        parsed_message.message_thread_id = message.reply_to.reply_to_msg_id
                    parsed_message.is_topic_message = True

            return parsed_message

        if isinstance(message, raw_types.Message):
            message_thread_id = None
            entities = [pyrogram_types.MessageEntity._parse(client, entity, users) for entity in message.entities]
            entities = pyrogram_types.List(filter(lambda x: x is not None, entities))

            forward_from = None
            forward_sender_name = None
            forward_from_chat = None
            forward_from_message_id = None
            forward_signature = None
            forward_date = None
            is_topic_message = None

            forward_header = message.fwd_from

            if forward_header:
                forward_date = utils.timestamp_to_datetime(forward_header.date)
                if forward_header.from_id:
                    raw_peer_id = utils.get_raw_peer_id(forward_header.from_id)
                    peer_id = utils.get_peer_id(forward_header.from_id)
                    if peer_id > 0 and raw_peer_id in users:
                        forward_from = pyrogram_types.User._parse(client, users[raw_peer_id])
                    elif raw_peer_id in chats:
                        forward_from_chat = pyrogram_types.Chat._parse_channel_chat(client, chats[raw_peer_id])
                        forward_from_message_id = forward_header.channel_post
                        forward_signature = forward_header.post_author
                elif forward_header.from_name:
                    forward_sender_name = forward_header.from_name

            photo = None
            location = None
            contact = None
            venue = None
            game = None
            giveaway = None
            story = None
            audio = None
            voice = None
            animation = None
            video = None
            video_note = None
            sticker = None
            document = None
            web_page = None
            poll = None
            dice = None

            media = message.media
            media_type = None
            has_media_spoiler = None

            if media:
                if isinstance(media, raw_types.MessageMediaPhoto):
                    photo = pyrogram_types.Photo._parse(client, media.photo, media.ttl_seconds)
                    media_type = enums.MessageMediaType.PHOTO
                    has_media_spoiler = media.spoiler
                elif isinstance(media, raw_types.MessageMediaGeo):
                    location = pyrogram_types.Location._parse(client, media.geo)
                    media_type = enums.MessageMediaType.LOCATION
                elif isinstance(media, raw_types.MessageMediaContact):
                    contact = pyrogram_types.Contact._parse(client, media)
                    media_type = enums.MessageMediaType.CONTACT
                elif isinstance(media, raw_types.MessageMediaVenue):
                    venue = pyrogram_types.Venue._parse(client, media)
                    media_type = enums.MessageMediaType.VENUE
                elif isinstance(media, raw_types.MessageMediaGame):
                    game = pyrogram_types.Game._parse(client, message)
                    media_type = enums.MessageMediaType.GAME
                elif isinstance(media, raw_types.MessageMediaGiveaway):
                    giveaway = pyrogram_types.Giveaway._parse(client, media, chats)
                    media_type = enums.MessageMediaType.GIVEAWAY
                elif isinstance(media, raw_types.MessageMediaStory):
                    story = pyrogram_types.MessageStory._parse(client, media, users, chats)
                    media_type = enums.MessageMediaType.STORY
                elif isinstance(media, raw_types.MessageMediaDocument):
                    doc = media.document
                    if isinstance(doc, raw_types.Document):
                        attributes = {type(i): i for i in doc.attributes}
                        file_name = getattr(
                            attributes.get(raw_types.DocumentAttributeFilename, None), "file_name", ""
                        )
                        if raw_types.DocumentAttributeAnimated in attributes:
                            video_attributes = attributes.get(raw_types.DocumentAttributeVideo, None)
                            animation = pyrogram_types.Animation._parse(client, doc, video_attributes, file_name or "")
                            media_type = enums.MessageMediaType.ANIMATION
                            has_media_spoiler = media.spoiler
                        elif raw_types.DocumentAttributeSticker in attributes:
                            sticker = await pyrogram_types.Sticker._parse(client, doc, attributes)
                            media_type = enums.MessageMediaType.STICKER
                        elif raw_types.DocumentAttributeVideo in attributes:
                            video_attributes = attributes[raw_types.DocumentAttributeVideo]
                            if video_attributes.round_message:
                                video_note = pyrogram_types.VideoNote._parse(client, doc, video_attributes)
                                media_type = enums.MessageMediaType.VIDEO_NOTE
                            else:
                                video = pyrogram_types.Video._parse(client, doc, video_attributes, file_name or "", media.ttl_seconds)
                                media_type = enums.MessageMediaType.VIDEO
                                has_media_spoiler = media.spoiler
                        elif raw_types.DocumentAttributeAudio in attributes:
                            audio_attributes = attributes[raw_types.DocumentAttributeAudio]
                            if audio_attributes.voice:
                                voice = pyrogram_types.Voice._parse(client, doc, audio_attributes)
                                media_type = enums.MessageMediaType.VOICE
                            else:
                                audio = pyrogram_types.Audio._parse(client, doc, audio_attributes, file_name or "")
                                media_type = enums.MessageMediaType.AUDIO
                        else:
                            document = pyrogram_types.Document._parse(client, doc, file_name or "")
                            media_type = enums.MessageMediaType.DOCUMENT
                elif isinstance(media, raw_types.MessageMediaWebPage):
                    if isinstance(media.webpage, raw_types.WebPage):
                        web_page = pyrogram_types.WebPage._parse(client, media.webpage, media.force_large_media, media.force_small_media, media.manual)
                        media_type = enums.MessageMediaType.WEB_PAGE_PREVIEW
                    else:
                        media = None
                elif isinstance(media, raw_types.MessageMediaPoll):
                    poll = pyrogram_types.Poll._parse(client, media)
                    media_type = enums.MessageMediaType.POLL
                elif isinstance(media, raw_types.MessageMediaDice):
                    dice = pyrogram_types.Dice._parse(client, media)
                    media_type = enums.MessageMediaType.DICE
                else:
                    media = None

            reply_markup = message.reply_markup
            if reply_markup:
                if isinstance(reply_markup, raw_types.ReplyKeyboardForceReply):
                    reply_markup = pyrogram_types.ForceReply.read(reply_markup)
                elif isinstance(reply_markup, raw_types.ReplyKeyboardMarkup):
                    reply_markup = pyrogram_types.ReplyKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw_types.ReplyInlineMarkup):
                    reply_markup = pyrogram_types.InlineKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw_types.ReplyKeyboardHide):
                    reply_markup = pyrogram_types.ReplyKeyboardRemove.read(reply_markup)
                else:
                    reply_markup = None

            from_user = pyrogram_types.User._parse(client, users.get(user_id, None))
            sender_chat = pyrogram_types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None
            reactions = pyrogram_types.MessageReactions._parse(client, message.reactions)

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                effect_id=getattr(message, "effect", None),
                date=utils.timestamp_to_datetime(message.date),
                chat=pyrogram_types.Chat._parse(client, message, users, chats, is_chat=True),
                topics=None,
                from_user=from_user,
                sender_chat=sender_chat,
                text=(
                    Str(message.message).init(entities) or None
                    if media is None or web_page is not None
                    else None
                ),
                caption=(
                    Str(message.message).init(entities) or None
                    if media is not None and web_page is None
                    else None
                ),
                entities=(
                    entities or None
                    if media is None or web_page is not None
                    else None
                ),
                caption_entities=(
                    entities or None
                    if media is not None and web_page is None
                    else None
                ),
                author_signature=message.post_author,
                has_protected_content=message.noforwards,
                has_media_spoiler=has_media_spoiler,
                forward_from=forward_from,
                forward_sender_name=forward_sender_name,
                forward_from_chat=forward_from_chat,
                forward_from_message_id=forward_from_message_id,
                forward_signature=forward_signature,
                forward_date=forward_date,
                is_topic_message=is_topic_message,
                mentioned=message.mentioned,
                scheduled=is_scheduled,
                from_scheduled=message.from_scheduled,
                media=media_type,
                edit_hide=message.edit_hide,
                invert_media=getattr(message, "invert_media", None),
                edit_date=utils.timestamp_to_datetime(message.edit_date),
                media_group_id=message.grouped_id,
                photo=photo,
                location=location,
                contact=contact,
                venue=venue,
                audio=audio,
                voice=voice,
                animation=animation,
                game=game,
                giveaway=giveaway,
                story=story,
                video=video,
                video_note=video_note,
                sticker=sticker,
                document=document,
                web_page=web_page,
                poll=poll,
                dice=dice,
                views=message.views,
                forwards=message.forwards,
                via_bot=pyrogram_types.User._parse(client, users.get(message.via_bot_id, None)),
                outgoing=message.out,
                reply_markup=reply_markup,
                reactions=reactions,
                client=client
            )

            if message.reply_to:
                if isinstance(message.reply_to, raw_types.MessageReplyHeader):
                    if message.reply_to.quote:
                        parsed_message.quote = pyrogram_types.TextQuote._parse(client, users, message.reply_to)
                    if message.reply_to.forum_topic:
                        if message.reply_to.reply_to_top_id:
                            thread_id = message.reply_to.reply_to_top_id
                            parsed_message.reply_to_message_id = message.reply_to.reply_to_msg_id
                        else:
                            thread_id = message.reply_to.reply_to_msg_id
                        parsed_message.message_thread_id = thread_id
                        parsed_message.is_topic_message = True
                        if topics and thread_id in topics:
                            parsed_message.topic = pyrogram_types.ForumTopic._parse(topics[thread_id])
                        else:
                            try:
                                if parsed_message.chat:
                                    msg = await client.get_messages(parsed_message.chat.id, message.id)
                                    if isinstance(msg, Message) and getattr(msg, "topic"):
                                        parsed_message.topic = msg.topic
                            except Exception:
                                pass
                    else:
                        parsed_message.reply_to_message_id = message.reply_to.reply_to_msg_id
                        parsed_message.reply_to_top_message_id = message.reply_to.reply_to_top_id
                else:
                    parsed_message.reply_to_story_id = message.reply_to.story_id
                    if isinstance(message.reply_to.peer, raw_types.PeerUser):
                        parsed_message.reply_to_story_user_id = message.reply_to.peer.user_id
                    elif isinstance(message.reply_to.peer, raw_types.PeerChat):
                        parsed_message.reply_to_story_chat_id = utils.get_channel_id(message.reply_to.peer.chat_id)
                    else:
                        parsed_message.reply_to_story_chat_id = utils.get_channel_id(message.reply_to.peer.channel_id)

                if replies:
                    if parsed_message.reply_to_message_id:
                        is_cross_chat = getattr(message.reply_to, "reply_to_peer_id", None) and getattr(message.reply_to.reply_to_peer_id, "channel_id", None)
                        if is_cross_chat:
                            key = (utils.get_channel_id(message.reply_to.reply_to_peer_id.channel_id), message.reply_to.reply_to_msg_id)
                            reply_to_params = {"chat_id": key[0], 'message_ids': key[1]}
                        else:
                            key = (parsed_message.chat.id if parsed_message.chat else 0, parsed_message.reply_to_message_id)
                            reply_to_params = {'chat_id': key[0], 'reply_to_message_ids': message.id}

                        try:
                            reply_to_message = client.message_cache[key]
                            if not reply_to_message:
                                try:
                                    reply_to_message = await client.get_messages(replies=replies - 1, **reply_to_params)
                                except (FloodWait, FloodPremiumWait) as e:
                                    await asyncio.sleep(e.value)
                                    reply_to_message = await client.get_messages(replies=replies - 1, **reply_to_params)
                                except ChannelPrivate:
                                    pass
                            if isinstance(reply_to_message, Message) and not reply_to_message.forum_topic_created:
                                parsed_message.reply_to_message = reply_to_message
                        except MessageIdsEmpty:
                            pass
                    elif parsed_message.reply_to_story_id and parsed_message.reply_to_story_user_id:
                        try:
                            reply_to_story = await client.get_stories(parsed_message.reply_to_story_user_id, parsed_message.reply_to_story_id)
                            parsed_message.reply_to_story = reply_to_story
                        except Exception:
                            pass

            if not parsed_message.poll and parsed_message.chat is not None:
                client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            return parsed_message

    def listen(
        self,
        filters: Any = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        timeout: Optional[int] = None,
        unallowed_click_alert: bool = True,
        user_id: Union[int, str, List[Union[int, str]], None] = None,
        message_id: Union[int, List[int], None] = None,
        inline_message_id: Union[str, List[str], None] = None,
    ) -> Any:
        return self._client.listen(
            chat_id=self.chat.id if self.chat else None,
            filters=filters,
            listener_type=listener_type,
            timeout=timeout,
            unallowed_click_alert=unallowed_click_alert,
            user_id=user_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

    def ask(
        self,
        text: str,
        filters: Any = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        timeout: Optional[int] = None,
        unallowed_click_alert: bool = True,
        user_id: Union[int, str, List[Union[int, str]], None] = None,
        message_id: Union[int, List[int], None] = None,
        inline_message_id: Union[str, List[str], None] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if not self.chat:
            raise ValueError()
        return self._client.ask(
            chat_id=self.chat.id,
            text=text,
            filters=filters,
            listener_type=listener_type,
            timeout=timeout,
            unallowed_click_alert=unallowed_click_alert,
            user_id=user_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            *args,
            **kwargs,
        )

    def stop_listening(
        self,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        user_id: Union[int, str, List[Union[int, str]], None] = None,
        message_id: Union[int, List[int], None] = None,
        inline_message_id: Union[str, List[str], None] = None,
    ) -> Any:
        return self._client.stop_listening(
            chat_id=self.chat.id if self.chat else None,
            listener_type=listener_type,
            user_id=user_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

    @property
    def link(self) -> str:
        if not self.chat:
            return ""
        if (
            self.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)
            and self.chat.username
        ):
            return f"https://t.me/{self.chat.username}/{self.id}"
        else:
            return f"https://t.me/c/{utils.get_channel_id(self.chat.id)}/{self.id}"

    async def get_media_group(self) -> List[Message]:
        if not self.chat:
            return []
        result = await self._client.get_media_group(chat_id=self.chat.id, message_id=self.id)
        return cast(List[Message], result)

    async def reply_text(
        self,
        text: str,
        quote: Optional[bool] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        schedule_date: Optional[datetime] = None,
        protect_content: Optional[bool] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            protect_content=protect_content,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    reply = reply_text

    async def reply_animation(
        self,
        animation: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        caption: str = "",
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_animation(
            chat_id=self.chat.id,
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def reply_audio(
        self,
        audio: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        caption: str = "",
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        duration: int = 0,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_audio(
            chat_id=self.chat.id,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def reply_cached_media(
        self,
        file_id: str,
        quote: Optional[bool] = None,
        caption: str = "",
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_cached_media(
            chat_id=self.chat.id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def reply_chat_action(self, action: enums.ChatAction) -> bool:
        if not self.chat:
            return False
        return await self._client.send_chat_action(
            chat_id=self.chat.id,
            action=action
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        quote: Optional[bool] = None,
        last_name: str = "",
        vcard: str = "",
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_contact(
            chat_id=self.chat.id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def reply_document(
        self,
        document: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        thumb: Optional[str] = None,
        caption: str = "",
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        file_name: Optional[str] = None,
        force_document: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        schedule_date: Optional[datetime] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_document(
            chat_id=self.chat.id,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            file_name=file_name,
            force_document=force_document,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def reply_game(
        self,
        game_short_name: str,
        quote: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_game(
            chat_id=self.chat.id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def reply_inline_bot_result(
        self,
        query_id: int,
        result_id: str,
        quote: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_inline_bot_result(
            chat_id=self.chat.id,
            query_id=query_id,
            result_id=result_id,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities
        )
        return cast(Message, result)

    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        quote: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_location(
            chat_id=self.chat.id,
            latitude=latitude,
            longitude=longitude,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def reply_media_group(
        self,
        media: List[Union[
            pyrogram_types.InputMediaPhoto,
            pyrogram_types.InputMediaVideo,
            pyrogram_types.InputMediaAudio,
            pyrogram_types.InputMediaDocument
        ]],
        quote: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None
    ) -> List[pyrogram_types.Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_media_group(
            chat_id=self.chat.id,
            media=media,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities
        )
        return cast(List[pyrogram_types.Message], result)

    async def reply_photo(
        self,
        photo: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        caption: str = "",
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        ttl_seconds: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def reply_poll(
        self,
        question: str,
        options: List[str],
        is_anonymous: bool = True,
        type: enums.PollType = enums.PollType.REGULAR,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[enums.ParseMode] = None,
        explanation_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[datetime] = None,
        is_closed: Optional[bool] = None,
        quote: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        schedule_date: Optional[datetime] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_poll(
            chat_id=self.chat.id,
            question=question,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def reply_sticker(
        self,
        sticker: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_sticker(
            chat_id=self.chat.id,
            sticker=sticker,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def reply_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        quote: Optional[bool] = None,
        foursquare_id: str = "",
        foursquare_type: str = "",
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_venue(
            chat_id=self.chat.id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def reply_video(
        self,
        video: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        caption: str = "",
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        ttl_seconds: Optional[int] = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Optional[str] = None,
        supports_streaming: bool = True,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_video(
            chat_id=self.chat.id,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def reply_video_note(
        self,
        video_note: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        duration: int = 0,
        length: int = 1,
        thumb: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_video_note(
            chat_id=self.chat.id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def reply_voice(
        self,
        voice: Union[str, BinaryIO],
        quote: Optional[bool] = None,
        caption: str = "",
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        duration: int = 0,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = None,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Message]:
        if not self.chat:
            raise ValueError()
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id
        result = await self._client.send_voice(
            chat_id=self.chat.id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
        return cast(Optional[Message], result)

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional[enums.ParseMode] = None,
        entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[pyrogram_types.InlineKeyboardMarkup] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        result = await self._client.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    edit = edit_text

    async def edit_caption(
        self,
        caption: str,
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        reply_markup: Optional[pyrogram_types.InlineKeyboardMarkup] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        result = await self._client.edit_message_caption(
            chat_id=self.chat.id,
            message_id=self.id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def edit_media(
        self,
        media: pyrogram_types.InputMedia,
        reply_markup: Optional[pyrogram_types.InlineKeyboardMarkup] = None,
        file_name: Optional[str] = None
    ) -> Message:
        if not self.chat:
            raise ValueError()
        result = await self._client.edit_message_media(
            chat_id=self.chat.id,
            message_id=self.id,
            media=media,
            reply_markup=reply_markup,
            file_name=file_name,
        )
        return cast(Message, result)

    async def edit_reply_markup(self, reply_markup: Optional[pyrogram_types.InlineKeyboardMarkup] = None) -> Message:
        if not self.chat:
            raise ValueError()
        result = await self._client.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.id,
            reply_markup=reply_markup
        )
        return cast(Message, result)

    async def forward(
        self,
        chat_id: Union[int, str],
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        schedule_date: Optional[datetime] = None
    ) -> Union[pyrogram_types.Message, List[pyrogram_types.Message]]:
        if not self.chat:
            raise ValueError()
        result = await self._client.forward_messages(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_ids=self.id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            schedule_date=schedule_date
        )
        return cast(Union[pyrogram_types.Message, List[pyrogram_types.Message]], result)

    async def copy(
        self,
        chat_id: Union[int, str],
        caption: Optional[str] = None,
        parse_mode: Optional[enums.ParseMode] = None,
        caption_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        reply_to_chat_id: Union[int, str, None] = None,
        reply_to_message_id: Optional[int] = None,
        quote_text: Optional[str] = None,
        quote_entities: Optional[List[pyrogram_types.MessageEntity]] = None,
        schedule_date: Optional[datetime] = None,
        protect_content: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        reply_markup: Optional[Union[
            pyrogram_types.InlineKeyboardMarkup,
            pyrogram_types.ReplyKeyboardMarkup,
            pyrogram_types.ReplyKeyboardRemove,
            pyrogram_types.ForceReply
        ]] = cast(Any, object)
    ) -> Union[pyrogram_types.Message, List[pyrogram_types.Message]]:
        if not self.chat:
            raise ValueError()
        if self.service:
            log.warning("Service messages cannot be copied. chat_id: %s, message_id: %s", self.chat.id, self.id)
            raise ValueError()
        elif self.game and not await self._client.storage.is_bot():
            log.warning("Users cannot send messages with Game media type. chat_id: %s, message_id: %s", self.chat.id, self.id)
            raise ValueError()
        elif self.empty:
            log.warning("Empty messages cannot be copied.")
            raise ValueError()
        elif self.text:
            result = await self._client.send_message(
                chat_id,
                text=self.text,
                entities=self.entities,
                parse_mode=enums.ParseMode.DISABLED,
                disable_web_page_preview=not self.web_page,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_chat_id=reply_to_chat_id,
                reply_to_message_id=reply_to_message_id,
                quote_text=quote_text,
                quote_entities=quote_entities,
                schedule_date=schedule_date,
                protect_content=protect_content,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )
            return cast(pyrogram_types.Message, result)
        elif self.media:
            send_media = partial(
                self._client.send_cached_media,
                chat_id=chat_id,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_message_id=reply_to_message_id,
                quote_text=quote_text,
                quote_entities=quote_entities,
                schedule_date=schedule_date,
                protect_content=protect_content,
                has_spoiler=has_spoiler,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )

            if self.photo:
                file_id = self.photo.file_id
            elif self.audio:
                file_id = self.audio.file_id
            elif self.document:
                file_id = self.document.file_id
            elif self.video:
                file_id = self.video.file_id
            elif self.animation:
                file_id = self.animation.file_id
            elif self.voice:
                file_id = self.voice.file_id
            elif self.sticker:
                file_id = self.sticker.file_id
            elif self.video_note:
                file_id = self.video_note.file_id
            elif self.contact:
                contact_res = await self._client.send_contact(
                    chat_id,
                    phone_number=self.contact.phone_number,
                    first_name=self.contact.first_name,
                    last_name=self.contact.last_name,
                    vcard=self.contact.vcard,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date
                )
                return cast(pyrogram_types.Message, contact_res)
            elif self.location:
                loc_res = await self._client.send_location(
                    chat_id,
                    latitude=self.location.latitude,
                    longitude=self.location.longitude,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date
                )
                return cast(pyrogram_types.Message, loc_res)
            elif self.venue:
                venue_res = await self._client.send_venue(
                    chat_id,
                    latitude=self.venue.location.latitude,
                    longitude=self.venue.location.longitude,
                    title=self.venue.title,
                    address=self.venue.address,
                    foursquare_id=self.venue.foursquare_id,
                    foursquare_type=self.venue.foursquare_type,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date
                )
                return cast(pyrogram_types.Message, venue_res)
            elif self.poll:
                poll_res = await self._client.send_poll(
                    chat_id,
                    question=self.poll.question,
                    options=[opt.text for opt in self.poll.options],
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date
                )
                return cast(pyrogram_types.Message, poll_res)
            elif self.game:
                game_res = await self._client.send_game(
                    chat_id,
                    game_short_name=self.game.short_name,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id
                )
                return cast(pyrogram_types.Message, game_res)
            else:
                raise ValueError()

            if self.sticker or self.video_note:
                final_res = await send_media(
                    file_id=file_id,
                    message_thread_id=message_thread_id
                )
                return cast(pyrogram_types.Message, final_res)
            else:
                if caption is None:
                    caption = self.caption or ""
                    caption_entities = self.caption_entities
                final_res = await send_media(
                    file_id=file_id,
                    caption=caption,
                    parse_mode=parse_mode,
                    caption_entities=caption_entities,
                    message_thread_id=message_thread_id
                )
                return cast(pyrogram_types.Message, final_res)
        else:
            raise ValueError()

    async def delete(self, revoke: bool = True) -> bool:
        if not self.chat:
            return False
        result = await self._client.delete_messages(
            chat_id=self.chat.id,
            message_ids=self.id,
            revoke=revoke
        )
        return bool(result)

    async def click(
        self,
        x: Union[int, str] = 0,
        y: Optional[int] = None,
        quote: Optional[bool] = None,
        timeout: int = 10
    ) -> Any:
        if isinstance(self.reply_markup, pyrogram_types.ReplyKeyboardMarkup):
            keyboard = self.reply_markup.keyboard
            is_inline = False
        elif isinstance(self.reply_markup, pyrogram_types.InlineKeyboardMarkup):
            keyboard = self.reply_markup.inline_keyboard
            is_inline = True
        else:
            raise ValueError()

        if isinstance(x, int) and y is None:
            try:
                button = [button for row in keyboard for button in row][x]
            except IndexError:
                raise ValueError()
        elif isinstance(x, int) and isinstance(y, int):
            try:
                button = keyboard[y][x]
            except IndexError:
                raise ValueError()
        elif isinstance(x, str) and y is None:
            label = x.encode("utf-16", "surrogatepass").decode("utf-16")
            try:
                button = [button for row in keyboard for button in row if label == button.text][0]
            except IndexError:
                raise ValueError()
        else:
            raise ValueError()

        if is_inline:
            if isinstance(button, pyrogram_types.InlineKeyboardButton):
                if button.callback_data:
                    return await self._client.request_callback_answer(
                        chat_id=self.chat.id if self.chat else 0,
                        message_id=self.id,
                        callback_data=button.callback_data,
                        timeout=timeout
                    )
                elif button.url:
                    return button.url
                elif button.switch_inline_query:
                    return button.switch_inline_query
                elif button.switch_inline_query_current_chat:
                    return button.switch_inline_query_current_chat
                else:
                    raise ValueError()
            else:
                raise ValueError()
        else:
            text_to_reply = button.text if isinstance(button, pyrogram_types.KeyboardButton) else str(button)
            return await self.reply(text_to_reply, quote=quote)

    async def react(self, emoji: Union[int, str, None] = None, big: bool = False) -> bool:
        if not self.chat:
            return False
        return await self._client.send_reaction(
            chat_id=self.chat.id,
            message_id=self.id,
            emoji=emoji,
            big=big
        )

    async def retract_vote(self) -> pyrogram_types.Poll:
        if not self.chat:
            raise ValueError()
        result = await self._client.retract_vote(
            chat_id=self.chat.id,
            message_id=self.id
        )
        return cast(pyrogram_types.Poll, result)

    async def download(
        self,
        file_name: str = "",
        in_memory: bool = False,
        block: bool = True,
        progress: Optional[Callable[..., Any]] = None,
        progress_args: tuple[Any, ...] = ()
    ) -> Optional[Union[str, BinaryIO]]:
        return await self._client.download_media(
            message=self,
            file_name=file_name,
            in_memory=in_memory,
            block=block,
            progress=progress,
            progress_args=progress_args,
        )

    async def vote(self, option: int) -> pyrogram_types.Poll:
        if not self.chat:
            raise ValueError()
        result = await self._client.vote_poll(
            chat_id=self.chat.id,
            message_id=self.id,
            options=option
        )
        return cast(pyrogram_types.Poll, result)

    async def pin(self, disable_notification: bool = False, both_sides: bool = False) -> pyrogram_types.Message:
        if not self.chat:
            raise ValueError()
        result = await self._client.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id,
            disable_notification=disable_notification,
            both_sides=both_sides
        )
        return cast(pyrogram_types.Message, result)

    async def unpin(self) -> bool:
        if not self.chat:
            return False
        return await self._client.unpin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id
        )