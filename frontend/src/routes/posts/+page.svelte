<script lang="ts">
    import Feed from "$components/Post/feed.svelte";

    const temp_data = [
        {
            author: {
                name: "John Doe",
                profile_image: "https://picsum.photos/id/433/300/300",
                URL: "/",
                DegreeYear: "1",
                Degree: "Artificial Intelligence",
            },
            datetime: "1734491059",
            title: "Hello World",
            text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            likes: 0,
            images: ["https://picsum.photos/id/237/1920/1080", "https://picsum.photos/id/197/1920/1080", "https://picsum.photos/id/348/1920/1080"],
            tags: ["CampusLife", "LinkedInForStudents"],
            id: 1,
        },
        {
            author: {
                name: "Jane Smith",
                profile_image: "https://picsum.photos/id/582/300/300",
                URL: ""
            },
            datetime: "1741894311",
            title: "Another Post",
            text: "Another example of a post with some dummy text. This is just to show how multiple posts can be rendered on the page.",
            likes: 5,
            tags: ["CampusEats"],
            id: 2,
        },
        {
            author: {
                name: "Jake Stuckey",
                profile_image: "https://picsum.photos/seed/c/300/300",
                URL: "",
                DegreeYear: "4",
                Degree: "Building Information Modelling (BIM) in Design Construction and Operations",
            },
            title: "Third Post",
            datetime: "1741894312",
            text: "This is the third post in the list. It is a bit shorter than the previous ones, but it still serves the purpose of showing how the posts are rendered.",
            images: ["https://picsum.photos/seed/bbx/1920/1080"],
            likes: 2,
            tags: ["Academics & Studying", "Extracurricular Activities","College Finance & Budgeting"],
            id: 3,
        },
        {
            author: {
                name: "Kane Hill",
                profile_image: "https://picsum.photos/seed/d/300/300",
                URL: "",
                DegreeYear: "3",
                Degree: "Journalism",
            },
            title: "",
            datetime: "1741894313",
            images: ["https://picsum.photos/seed/c/1920/1080"],
            likes: 99,
            tags: ["SleepDeprivedStudents"],
            id: 4,
        },
        {
            author: {
                name: "Kane Hill",
                profile_image: "https://picsum.photos/seed/d/300/300",
                URL: "",
                DegreeYear: "3",
                Degree: "Journalism",
            },
            title: "",
            datetime: "1741894313",
            likes: 99,
            event: {
                title: "Cool Event",
                description: "Event Description",
                start_time: "1741894313",
                end_time: "1741894313",
                location: {
                    name: "4Q56",
                    lat: 51.501662,
                    lon: -2.548685,
                },
            },
            tags: ["Event"],
            id: 4,
        }
    ];



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
    <Feed data={temp_data}
        minColWidth={sliders[0].value}
        maxColWidth={sliders[1].value}
        gap={sliders[2].value}
        width={sliders[3].value}
        height={sliders[4].value}
    />
</div>
