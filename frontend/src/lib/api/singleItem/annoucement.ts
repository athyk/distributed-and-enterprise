import type { singleAnnoucementResponse,globalAnnouncementData } from '$lib/api/apiType';
import { getTagID } from '$lib/api/getTagID';
import { get } from '$lib/api/get';

export async function getSingleAnnouncement(communityID: number, postID: number) : Promise<globalAnnouncementData | undefined> {
    let response = (await get(
        'community/' + communityID + '/announcements/' + postID
    )) as singleAnnoucementResponse;
    if (response.success === true) {
        let newTags: [string, number][] = [];
        for (let i = 0; i < response.announcement.tags.length; i++) {
            newTags.push([response.announcement.tags[i] as string, await getTagID(response.announcement.tags[i] as string)]);
        }
        response.announcement.tags = newTags;
        return response.announcement;
    } else {
        console.error('Error fetching announcement data:', response.error_message);
    }
}