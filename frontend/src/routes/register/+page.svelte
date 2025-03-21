<script lang="ts">
	import AccountCard from '$components/AccountCard/base.svelte';
	import Page from '$components/AccountCard/RegisterPages/page.svelte';
	import type { RegiserResponse } from '$lib/api/apiType';
	import { post } from '$lib/api/post';

	let step = 1;
	let errorMessage = '';
	let password_comfirm_value = '';

	let email: [string, string, string] = ['', 'Email', 'Enter your email'];
	let password: [string, string, string] = ['', 'Password', 'Enter your password'];

	let first_name: [string, string, string] = ['', 'First Name', 'Enter your first name'];
	let last_name: [string, string, string] = ['', 'Last Name', 'Enter your last name'];
	let dob: [string, string, string] = ['', 'Date of Birth', 'Enter your date'];
	let gender: [string, string, string[]] = ['', 'Select Your Gender', ['Male', 'Female']];

	let degree: [[string, number][], string, string] = [[], 'degrees/list', 'Select Your Degree'];
	let year_of_study: [number, number, string] = [0, 5, 'Select Your Year of Study'];
	let graduation_date: [number, string] = [0, 'Select Your Graduation Year'];
	let tags: [[string, number][], string, string] = [[], 'tags/list', 'Select Your Tags'];

	function validateStep(currentStep: number): boolean {
		if (currentStep === 1) {
			if (email[0] === '' || password[0] === '') {
				errorMessage = 'Please fill in all fields';
				return false;
			}
			if (password[0] !== password_comfirm_value) {
				errorMessage = 'Passwords do not match ' + password[0] + ' ' + password_comfirm_value;
				return false;
			}
			if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email[0])) {
				errorMessage = 'Invalid email format';
				return false;
			}
		} else if (currentStep === 2) {
			if (first_name[0] === '' || last_name[0] === '' || dob[0] === '') {
				errorMessage = 'Please fill in all fields';
				return false;
			}
		}
		return true;
	}

	async function register() {
		if (!validateStep(step)) {
			return;
		}
		console.log(degree);
		const degreeId = degree[0].length > 0 ? degree[0][0][1] : null;
		const tagIds = tags[0].map((tag) => tag[1]);
		const dobDate = new Date(dob[0]);
		const dobString =
			('0' + dobDate.getDate()).slice(-2) +
			'-' +
			('0' + (dobDate.getMonth() + 1)).slice(-2) +
			'-' +
			dobDate.getFullYear();

		let data = {
			email: email[0],
			password: password[0],
			first_name: first_name[0],
			last_name: last_name[0],
			dob: dobString,
			gender: gender[0],
			degree_id: degreeId,
			year_of_study: year_of_study[0],
			grad_date: '30-06-' + graduation_date[0],
			tags: tagIds,
			skip_email: (document.getElementById('skip') as HTMLInputElement)?.checked
		};

		console.log('Registering: ', data);
		let response = (await post('auth/register', data)) as RegiserResponse;
		if (response.success) {
			if (response.otp_required) {
				errorMessage = 'OTP sent to your email';
				window.location.href = '/login?otp=true';
			}
			localStorage.setItem('userID', response.user_id.toString());
			// window.location.href = '/';
		} else {
			console.log('Error: ', response.error_message);

			errorMessage = '';
			for (let i = 0; i < response.error_message.length; i++) {
				if (i > 0) {
					errorMessage += ' | ';
				}
				errorMessage += response.error_message[i];
			}
		}
	}
</script>

<div class="flex h-screen w-full items-center justify-center">
	<AccountCard
		title="Register"
		subText="Create an account"
		imageUrl="https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
		promoteUrl="login"
		promoteText="Already have an account?"
		maxstep={3}
		submitFunction={register}
		bind:step
		bind:errorMessage
		validateStepFunction={validateStep}
	>
		<svelte:fragment slot="pages">
			{#if step === 1}
				<Page bind:email bind:password password_comfirm={true} bind:password_comfirm_value />
			{/if}
			{#if step === 2}
				<Page bind:first_name bind:last_name bind:dob bind:gender />
			{/if}
			{#if step === 3}
				<Page bind:degree bind:year_of_study bind:graduation_date bind:tags />
				<input type="checkbox" id="skip" />
			{/if}
		</svelte:fragment>
	</AccountCard>
</div>
