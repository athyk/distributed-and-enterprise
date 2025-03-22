<script lang="ts">
    import Post from "./base.svelte";
    import type { globalAnnouncementData } from "$lib/api/apiType.ts";

    import Title from "./Sections/title.svelte";
    import Text from "./Sections/text.svelte";
    import Tags from "./Sections/tags.svelte";

    export let data: globalAnnouncementData[] = []

    function converTimetoUnix(date: string) {
        const dateObj = new Date(date);
        const unixTime = Math.floor(dateObj.getTime() / 1000);
        return unixTime.toString();
    }

</script>

{#each data as announcement (announcement.id)}
    <Post
        author={{
            name: "Announcement Testing User",
            profile_image: "https://picsum.photos/id/433/300/300",
            URL: "/",
        }}
        date={converTimetoUnix(announcement.uploaded)}
        id={announcement.id}
        likes={0}
        showLikes={false}
        ownPost={false}
    >
        <Title>{announcement.title}</Title>
        <Tags tags={announcement.tags} />
        <Text>{announcement.description}</Text>
    </Post>
{/each}
