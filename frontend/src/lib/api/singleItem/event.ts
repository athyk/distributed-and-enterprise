import type { EventSingleResponse,EventDataResponse } from '$lib/api/apiType';
import { get } from '$lib/api/get';

export async function getEventData(id: number) : Promise<EventDataResponse | undefined> {
    let response = (await get('posts/?post_id=' + id)) as EventSingleResponse;
    if (response.success === true) {
        console.log(response.event);
        return response.event;
    } else {
        console.error('Error fetching post data:', response.error_message);
    }
}