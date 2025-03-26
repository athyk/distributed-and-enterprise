<script lang="ts">
    import Post from "./base.svelte";
    import type { globalAnnouncementData,globalAnnouncement } from "$lib/api/apiType.ts";
    import { get } from "$lib/api/get";
    import Title from "./Sections/title.svelte";
    import Text from "./Sections/text.svelte";
    import Tags from "./Sections/tags.svelte";

    import { onMount } from "svelte";

    export let url = '';

    let data: globalAnnouncementData[] = []

    function converTimetoUnix(date: string) {
        const dateObj = new Date(date);
        const unixTime = Math.floor(dateObj.getTime() / 1000);
        return unixTime.toString();
    }

    async function GetAnnouncments(){
        const response = await get(url) as globalAnnouncement
        if (response.http_status === 200) {
                data = response.global_announcements;
        } else {
            console.error("Error fetching announcements:", response.error_message);
            return [];
        }
    }

    onMount(() => {
        GetAnnouncments();
    });

</script>

{#each data as announcement (announcement.id)}
    <Post
        author={announcement.user}
        date={converTimetoUnix(announcement.uploaded)}
        id={announcement.id}
        ownPost={false}
    >
        <Title>{announcement.title}</Title>
        <Tags tags={announcement.tags} />
        <Text>{announcement.description}</Text>
    </Post>
{/each}
