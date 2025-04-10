import type { singlePostResponse,postsData } from '$lib/api/apiType';
import { getTagID } from '$lib/api/getTagID';
import { get } from '$lib/api/get';

export async function getPostData(id: number) : Promise<postsData | undefined> {
    let response = (await get('posts/?post_id=' + id)) as singlePostResponse;
    if (response.success === true) {
        let newTags: [string, number][] = [];
        for (let i = 0; i < response.post.tags.length; i++) {
            newTags.push([response.post.tags[i], await getTagID(response.post.tags[i])]);
        }
        response.post.tags = newTags;
        console.log('Post data fetched successfully:', response.post);
        return response.post;
    } else {
        console.error('Error fetching post data:', response.error_message);
    }
}