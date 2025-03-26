<script lang="ts">
    import Post from "./base.svelte";
    import Title from "./Sections/title.svelte";
    import Text from "./Sections/text.svelte";
    import Tags from "./Sections/tags.svelte";
    import Map from "./Sections/Map/map.svelte";
    import Time from "./Sections/time.svelte";

    import { onMount } from "svelte";

    import { get } from "$lib/api/get";

    import type { EventDataResponse,EventResponse } from "$lib/api/apiType";

    let data: EventDataResponse[] = [];
    export let url = '';

    async function GetPosts(){
        const response = await get(url) as EventResponse
        if (response.success === true) {
            data = response.global_events;
            console.log(data);
        } else {
            console.error("Error fetching posts:", response.error_message);
            return [];
        }
    }

    onMount(() => {
        GetPosts();
    });

</script>

{#each data as event (event.id)}
    <Post
        id={event.id}
        ownPost={false}
    >
        <Title>{event.title}</Title>
        <Time datetime={event.datetime}/>
        <Tags tags={event.tags} />


        <Text>
            {event.description}
        </Text>
        <Map
            lat={event.latitude}
            lon={event.longitude}
        />

    </Post>
{/each}