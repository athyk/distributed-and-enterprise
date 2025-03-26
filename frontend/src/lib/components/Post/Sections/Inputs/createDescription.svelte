<script lang="ts">
    export let text: string = "";
</script>

<textarea
    bind:value={text}
    placeholder="Description"
    class="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500  h-[155px]"
    required
></textarea>
