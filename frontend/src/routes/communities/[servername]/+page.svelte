<script lang="ts">
    import CommunitySidebar from '$components/communitySidebar/CommunitySidebar.svelte';
  

  
    export let communitiesInfo: { 
      id: number; 
      name: string; 
      imageUrl?: string;
    }[] = [
      {
        id: 1,
        name: "Tech Innovators",
        imageUrl: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=100&q=60"
      },
      {
        id: 2,
        name: "Art Lovers",
        imageUrl: "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=100&q=60"
      },
      {
        id: 3,
        name: "Gaming Gurus",
        imageUrl: "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=100&q=60"
      }
    ];
  </script>
  
  <CommunitySidebar 
   
    {communitiesInfo}
  />
  