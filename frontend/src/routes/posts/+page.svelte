<script lang="ts">
	import Annoucements from "$components/Post/annoucements.svelte";
    import Feed from "$components/Post/feed.svelte";
	import Post from "$components/Post/post.svelte";
	import type { globalAnnouncement, globalAnnouncementData, postResponse, postsData } from "$lib/api/apiType.ts";
    import { get } from "$lib/api/get";
	import { onMount } from "svelte";


    let annoucements: globalAnnouncementData[] = [];
    let loading = true;

    async function GetAnnouncments(){
        const response = await get("community/announcements") as globalAnnouncement
        if (response.http_status === 200) {
            annoucements = response.global_announcements;
            loading = false;
        } else {
            console.error("Error fetching announcements:", response.error_message);
            return [];
        }
    }





    let sliders = [
        { id: "minColWidth", label: "Min Column Width", min: 100, max: 800, step: 10, value: 340 },
        { id: "maxColWidth", label: "Max Column Width", min: 300, max: 800, step: 10, value: 600 },
        { id: "gap", label: "Gap", min: 0, max: 50, step: 1, value: 0 },
        { id: "width", label: "Width", min: 600, max: 1920, step: 10, value: 1080 },
        { id: "height", label: "Height", min: 400, max: 1080, step: 10, value: 1920 }
    ];


</script>


<!-- <div class="settings-box p-4 bg-gray-100 rounded shadow-md mb-4">
    <h2 class="text-lg font-bold mb-2">Column Settings</h2>
    {#each sliders as setting}
        <div class="mb-2">
            <label for={setting.id} class="block text-sm font-medium">{setting.label}: {setting.value}px</label>
            <input
                id={setting.id}
                type="range"
                min={setting.min}
                max={setting.max}
                step={setting.step}
                bind:value={setting.value}
                class="w-full"
            />
        </div>
    {/each}
</div> -->



<div class="flex justify-center items-center min-h-screen">
    <Feed
        data={[1, 2, 3, 4, 5, 6]}
        minColWidth={sliders[0].value}
        maxColWidth={sliders[1].value}
        gap={sliders[2].value}
        width={sliders[3].value}
        height={sliders[4].value}
    >
        <Post url="posts/list?offset=0&limit=10" slot="Posts"/>
    </Feed>

</div>
