<script lang="ts">
    import Popup from '$components/ErrorPopUp/popup.svelte';

    export let title: string = "";
    export let subText: string = "";
    export let imageUrl: string = "";

    export let promoteUrl = "";
    export let promoteText = "";

    export let step = 1;
    export let maxstep = 1;

    export let submitFunction = () => {};

    export let errorMessage = '';

    export let validateStepFunction: ((currentStep: number) => boolean) | undefined = undefined;

    function handleStepChange(newStep: number) {
        if (newStep > step && validateStepFunction) {
            if (!validateStepFunction(step)) {
                return;
            }
        }
        step = newStep;
    }



</script>

<div
    class="mx-auto mt-5 flex min-h-[500px] md:w-1/2 sm:w-full overflow-hidden rounded-lg border border-black bg-white shadow-lg"
>
    {#if imageUrl}
        <div
            class="hidden w-1/3 bg-cover md:block"
            style="background-image: url('{imageUrl}')"
        ></div>
    {/if}
    <div class="w-full p-8 md:mx-auto md:w-1/2 flex flex-col">

        <div class="flex-grow">
            <h2 class="text-center text-2xl font-semibold text-gray-700">{title}</h2>
            <Popup bind:errorMessage />
            <p class="text-center text-xl text-gray-600">{subText}</p>
            <div class="mt-5 mb-5 overflow-auto p-2 h-[380px]">
                <slot name="pages"/>
            </div>

        </div>

        <footer class="mt-auto pt-4 flex flex-col items-center justify-between space-y-2 md:flex-row md:space-y-0">
            {#if step === 1}
                {#if promoteUrl}
                    <a href="/{promoteUrl}" class="text-sm text-bold text-gray-600 hover:text-gray-900">
                        {promoteText}
                    </a>
                {/if}
            {/if}
            {#if step != 1}
                <button class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900" on:click={() => (step = Math.max(1, step - 1))}>
                    Previous Step
                </button>
            {/if}
            {#if step != maxstep}
                <button class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900" on:click={() => handleStepChange(Math.min(maxstep, step + 1))}>
                    Next Step
                </button>
            {/if}
            {#if step == maxstep}
                <button class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900" on:click={submitFunction}>
                    Submit
                </button>
            {/if}

        </footer>
    </div>
</div>
