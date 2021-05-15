## Assumptions

## General

1. Exceptions are raised in the order that they appear listed in the spec.

## auth\_\* functions

1. Errors raised come in order of errors listed on the assignment specification
2. A user does not remain 'logged-in' so if user logs in twice, no error will be returned - so the return value will be the same both times the user attempts to log in
3. An error will be raised if the email provided to password/reset/request is not associated with a user
4. An error will be raised if no users have requested a password reset and one attempts to change their password

## channel_invite_v2

1. Assume channel_invite_v1 is able to invite users into private channels.
2. Assume channel_invite_v1 only adds users once to the channel so that there
   can only be a maximum of one entry per unique user in the channel's
   all_members list. If the user is already in the channel, channel_invite_v1
   should still return {}.
3. Assume users cannot invite themselves to the channel.

## channel_details_v2

1. Assume channel_details can reveal details of private channels as well.

## channels_list_v2 and channels_list_all_v2

1. Assume that private and public channels are treated the same in that they
   are both displayed when showing the list of channels that the user is a part
   off

## channel_join_v2

1. A user will never try to join a channel in which they are already a member (hence will not be tested for).
2. Owners of Dreams are not necessarily owners of any channel they join (not for this iteration).

## channel_messages_v2

1. "start" is an integer no less than 0, and won't be tested for
2. Messages are stored in the data structure as a queue, so this queue must be reversed to ensure the most recent message returned is given index 0

## admin_userpermission_change_v1

1. Assume owners are able to change their own permission to member
   permissions.
2. Assume if there is only one Owner of Dreams, they are not able to change
   their own permission to 2.
3. Assume owners are able to set the new permissions of others and
   themselves to be the same permissions they already had, with no errors
   occurring.

## admin_user_remove_v1
1. Assume users with owner permissions are able to remove themselves as long as they are not the only owner remaining.

## notifications_get_v1_test
1. Assume that if a user has 0 notifications, then notifications_get_v1_test will return a dictionary containing an empty list.
2. Assume users can tag themselves and receive notifications.
3. Assume users can be tagged even with a comma after their handle string
4. Users won't send a notification to themselves when they create a dm

## channel_addowner_v1

1. An invalid u_id will throw an InputError
2. Users can be made owners of channels they are not initially members of
3. Global owners can add owners in channels they are not a member of

## channel_removeowner_v1

1. A global owner can remove an owner of a channel even if the global owner is not a member of said channel.

## channel_leave_v1

1. Anyone can leave the channel, but the last owner will never try to leave
   (to align with the specification of channel_removeowner_v1) -> (InputError)

## search_v2

1. Will only search for messages in channels/dms that the user is currently a member of
   (i.e. does not consider channels/dms they have left)
2. Looks for substrings (i.e. is query_str a substring of a message?)
3. An empty query_str throws in an InputError

## user_set_handle

1. Any handle passed in that contains the '@' character or whitespace raises an input error

## user_ stat / user_stats

1. Lists are not initially empty but filled with 0 counts and associated timestamps

## dm_leave && dm_invite

1. The name of the dm will stay as the same when it is created. Even when people are added into or leave the dm, the dm name stays the same.
2. If the owner of dm leaves the dm without destroying it, the next owner of the dm will be picked up randomly between the left members. If the last member leaves the dm and there is no members left in the dm , the dm will automatically been removed.

## messages.py
1. Assumed deleted messages cannot be retrieved, and once it is deleted it's id can be reused.
2. For shared messages - the extra message is included in the shared message and is put on a new line after the contents of the message being shared.
3. Errors occur in order as defined in the spec
4. A user cannot share a message from a channel they are no a part of - this will result in an access error.
5. For channels: Channel names can be reused, so multiple channels can have the same name

## message_sendlater & message_sendlaterdm

1. The time_created of the message will be the time it is sent in the future (time_sent), not the actual time of creation.
2. A user will not try to leave the channel/dm before the message is delivered.