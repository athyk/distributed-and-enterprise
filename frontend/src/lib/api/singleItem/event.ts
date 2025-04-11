import type { EventSingleResponse, EventDataResponse } from '$lib/api/apiType';
import { getTagID } from '$lib/api/getTagID';
import { get } from '$lib/api/get';

export async function getEventData(
	communityID: number,
	eventID: number
): Promise<EventDataResponse | undefined> {
	const response = (await get(
		'community/' + communityID + '/events/' + eventID
	)) as EventSingleResponse;
	if (response.success === true) {
		const newTags: [string, number][] = [];
		for (let i = 0; i < response.event.tags.length; i++) {
			newTags.push([
				response.event.tags[i] as string,
				await getTagID(response.event.tags[i] as string)
			]);
		}
		response.event.tags = newTags;
		return response.event;
	} else {
		console.error('Error fetching post data:', response.error_message);
	}
}
