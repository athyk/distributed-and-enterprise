<script lang="ts">
    export let title: string = "";
</script>

<input
    type="text"
    bind:value={title}
    placeholder="Title"
    class="w-full border-2 border-gray-300 rounded-lg p-2 focus:outline-none focus:border-blue-500"
    required
/>