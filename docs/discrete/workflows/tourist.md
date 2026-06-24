## Is EdgeFirst Studio for you?

<div class="grid" markdown="1">

{{ video("/getting_started/assets/workflows/auto-labelling.mp4", "Auto-Labelling — AI-generated bounding boxes and segmentation masks") }}
{{ video("/getting_started/assets/workflows/model-optimization.mp4", "Model Optimization — train, compare, and benchmark vision models") }}
{{ video("/getting_started/assets/workflows/3d_perception.mp4", "3D Perception — LiDAR, RADAR, and depth sensor workflows") }}
{{ video("/getting_started/assets/workflows/profiler.mp4", "EdgeFirst Profiler — on-target benchmarking with latency and accuracy metrics") }}

</div>

EdgeFirst Studio is designed for teams and individuals building AI-powered products for the edge. If any of the following sounds familiar, you're in the right place:

- **You want to train and deploy vision models** without managing your own training infrastructure
- **You work with edge hardware** — cameras, NPUs, embedded systems — and need models that actually run fast on device
- **You need to manage datasets** — annotate, version, audit, and share image or sensor data across a team
- **You want to benchmark models on real hardware** and see accuracy alongside latency, not just one or the other
- **You're evaluating pre-trained models** and want to compare them against your own fine-tuned results
- **You're building a Physical AI system** with 3D sensors (LiDAR, RADAR, depth) alongside cameras

EdgeFirst Studio is a fully managed cloud platform — no servers to provision, no training clusters to maintain. You bring your data and your target hardware; Studio handles the rest.

!!! tip "Not sure yet?"
    No account needed to start exploring. Visit the {{ studio_link("EdgeFirst Studio landing page") }} to browse features and the public Model Zoo — then sign up when you're ready. New accounts start with **\$50 USD in free credits**.

## Explore EdgeFirst Studio

EdgeFirst Studio is accessible at {{ studio_link("edgefirst.studio") }}.  Upon visiting, you will see the EdgeFirst Studio landing page with an overview of the platform's features and capabilities — no account or sign-up is required to explore this page.

On the landing page you can:

- View the EdgeFirst Studio feature overview and product highlights
- Browse publicly available sample models in the [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models)
- Browse publicly available {{ studio_link("projects and datasets", "project") }}
- Learn about the EdgeFirst Perception ecosystem and supported target hardware

{{ figure("/getting_started/assets/studio_landing_page.jpg", "EdgeFirst Studio Landing Page") }}

## Platform Features

Use the table below as a quick overview of what is visible on the landing page.

| Feature | Description |
| --- | --- |
| Auto-labelling | Generate 2D and 3D bounding boxes and segmentation masks from video, frame sequences, MCAP, or other formats using AI-based Ground Truth generation. |
| 3D Perception and Physical AI | Built-in support for LiDAR, RADAR, point cloud, depth maps, and other 3D sensors with editing and auditing workflows. |
| Optimize Models | Train radar and vision models (including fusion), run parallel experiments, and compare results. |
| Validation | Review model performance and compare results across experiments across targets. |
| Deployment Targets | Deploy to Maivin, Raivin, i.MX 8M Plus, i.MX 95, NVIDIA Jetson Orin, Kinara ARA-2, Hailo platforms. |
| Public Datasets | Host and access public datasets. |
| Model Benchmarking | Benchmark and profile models on edge platforms and analyze performance. |
