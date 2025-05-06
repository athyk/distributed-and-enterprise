<script lang="ts">
    import { onMount } from 'svelte';
    import { getUserInfo } from '$lib/api/checkUser';
	import type { MeResponse } from '$lib/api/apiType';
	import { getDegreeName } from '$lib/api/getDegreeID';
	import {getTagName} from '$lib/api/getTagID';

    export let user_id = 1;
    let userInfo:MeResponse;
    let degree_name: string | undefined = undefined;

    async function formatDegree(degree_id: number | string) {
		try {
			if (typeof degree_id === 'number') {
				degree_id = degree_id.toString();
			}
			const result = await getDegreeName(degree_id);
			degree_name = result !== -1 ? result : undefined;
		} catch (error) {
			console.error('Error fetching degree name:', error);
		}
	}


	onMount(async () => {
		const response = (await getUserInfo()) as MeResponse;
		if (response.success === true) {
			user_id = response.user.id;
			userInfo = response;
			formatDegree(userInfo.user.degree_id);
		} else {
			console.error('Error fetching user info:', response.error_message);
		}
	});
</script>


{#if userInfo}
<div class="mb-4 flex flex-col sm:flex-row items-center sm:items-start border-b border-gray-300 pb-4 pt-5 gap-3">
    <div class="flex-shrink-0 mb-2 sm:mb-0">
        {#if userInfo.user.picture_url}
            <img src={userInfo.user.picture_url} alt="Profile" class="h-16 w-16 sm:h-20 sm:w-20 rounded-full border-2 border-gray-200" />
        {:else}
            <img src="https://picsum.photos/id/63/200/200" alt="Profile" class="h-16 w-16 sm:h-20 sm:w-20 rounded-full border-2 border-gray-200" />
        {/if}
    </div>
    <div class="flex flex-col text-center sm:text-left">
        <h1 class="text-xl sm:text-2xl font-bold">{userInfo.user.first_name} {userInfo.user.last_name}</h1>
        <p class="text-gray-700">Year {userInfo.user.year_of_study} {degree_name} Student</p>
    </div>
    <div class="mt-2 sm:mt-0 sm:ml-auto">
        <a href="/account/edit" class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 inline-block">
            Edit Account
        </a>
    </div>
</div>
<div class="mb-4 p-4 border border-gray-300 rounded-lg bg-gray-50">
    <ul class="space-y-3">
        <li><strong>Member Since:</strong> {new Date(Number(userInfo.user.created_at) * 1000).toLocaleDateString()}</li>
        <li>
            <strong>Tags:</strong> 
            <div class="flex flex-wrap gap-2 mt-1">
                {#if userInfo.user.tags?.length}
                    {#each userInfo.user.tags as tag, index}
                        {#await getTagName(tag.toString()) then tagName}
                            <span class="bg-gray-200 rounded-md px-2 py-1 text-sm">{tagName}</span>
                        {:catch error}
                            <span class="bg-red-200 rounded-md px-2 py-1 text-sm">Error</span>
                        {/await}
                    {/each}
                {:else}
                    <span>None</span>
                {/if}
            </div>
        </li>
        <li><strong>Gender:</strong> {userInfo.user.gender || 'Not specified'}</li>
    </ul>
</div>
{/if}