# Final Project Description

### Tammy Glazer and James Jensen

## Project Background

Since the mid-1990s, floods, storms, and earthquakes have made up nearly 80% of natural disasters around the world. Increasing global surface temperatures are leading to rising sea levels and the evaporation of excess water vapor into the atmosphere, increasing the likelihood of weather-driven disasters. As a direct result, locations including the Caribbean, Central America, the South Pacific, and the Himalayas face an elevated risk of experiencing natural hazards. While a variety of government and development organizations support emergency management and the provision of relief services, far less is being done by way of risk reduction and the development of data-driven resource prioritization strategies.  
  
In the face of a natural hazard, roof design, condition, and material contribute to household resilience. The traditional approach to identifying high-risk buildings and roofs in disaster prone locations involves going door-to-door to visually inspect building conditions, which can be extremely costly and time consuming. For instance, for windstorm mitigation inspections, an inspector will look for construction features that have been shown to reduce losses in hurricanes, such as concrete blocks, the presence of roof-to-wall attachments, and opening protections. An alternative approach would be to use high-resolution drone imagery to quickly identify, and in turn prioritize areas with problematic building materials. According to DrivenData, “Mapping a 10km2 neighborhood with a drone can be done within a matter of days and at a cost of a few thousand dollars at most” (2019).  
  
Earlier this year, we took a course in Unsupervised Machine Learning and used our final project as an opportunity to apply computer vision methods to address this challenge. Specifically, over the course of the quarter, we leveraged high definition, satellite imagery to identify and label rooftops by their construction materials. It was our hope that a successful labeling strategy for aerial imagery would facilitate the prioritization of building inspections in St. Lucia, Guatemala, and Colombia, thereby ensuring community resilience in high risk locations. We were specifically interested in how unsupervised learning techniques could be used to derive rooftop material labels when training data are unavailable.  

## Computing Challenges

The data consist of seven satellite images at 4cm resolution stored as Cloud Optimized GeoTIFFs (COGs), totaling over 60GB, as well as accompanying building footprints stored as GeoJSONs. All data are provided by WeRobotics and the World Bank Global Program for Resilient Housing. COGs can be hosted and accessed on an HTTP server. They have the potential to enable efficient workflows since HTTP get range requests can draw only upon necessary parts of each file. Without prior knowledge of large-scale computing strategies, however, we previously completed coordinate transformations, image masking and segmentation, image pre-processing, and feature generation serially. Further, we completed the entire analysis on our personal machines using locally stored images, making it difficult to share insights and impossible to access the data remotely. As a result of these challenges, downloading the data took approximately 6 hours, and data processing took well over 40 hours to complete.  

## Social Science Research Question

Our Social Science Research Question is the following: Can large-scale computing strategies be leveraged to expedite high-resolution satellite image acquisition and pre-processing to facilitate machine learning and improve disaster preparedness?  
  
Using our large-scale computing strategies, we seek to parallelize a majority of computer vision related data acquisition, pre-processing, and image preparation tasks to expedite our machine learning pipeline. In the case of an imminent natural emergency, it is critical that organizations be able to quickly target buildings for inspection as a disaster risk reduction strategy. A streamlined data processing workflow will enable our time-sensitive models to be productionized, thereby supporting humanitarian organizations and ensuring community resilience.  

## Large-Scale Computing Approaches

To expedite our feature generation process, were able to incorporate a variety of large-scale computing techniques into our data processing workflow. We begin by using a multi-part uploading technique (TransferConfig) to concurrently upload 7 large tif files to an AWS S3 bucket, ranging from 1.65 to 9.96 GB in size. We use this approach for two main reasons. First, threading of large image files can result in future data access challenges using serverless solutions such as AWS Lambda, making a concurrent solution preferable. Second, multi-part transfers are necessary when an individual file size exceeds a specified S3 bucket threshold, which we encountered. We were able to tune the maximum number of concurrent S3 API transfer operations based on our connection speed using the max_concurrency attribute.  

Next, we leverage a multithreading technique (ThreadPool) to upload 7 GeoJSONs to the same AWS S3 bucket. This is a parallel approach that allowed us to run multiple threads of execution within an operating system, thereby maximizing the capacity of our machine’s CPUs. As a result of these processes, we are both able to access the files using the Boto3, the AWS SDK for Python.  

For the remainder of our project, we parallelize image interaction, pre-processing, and feature generation for our machine learning models using   


-------NOTES FOLLOW-------



Segmentation, Pre-Processing, Feature Generation: Parallelize raster image computations using Pywren on top of AWS Lambda (optimized for computational imaging)

We propose parallelizing our workflow using a serverless solution such as Amazon Lambda via PyWren. We will also explore the feasibility and performance gains of using Amazon EMR, which uses EC2 instances and hosts data using S3 buckets. Time permitting, we are excited to explore whether we can incorporate Apache Spark into our workflow, which has the benefit of supporting scalable machine learning algorithms. Given the unique nature of our project, James Jensen and I received permission from Professor Clindaniel to work as a team on this effort.
Challenges: uploading large file, AWS Lambda has 512MB temp storage limit, making it difficult to map geojsons to the files
Findings

Graphs?

GOALS:
-Describe social science research problem
-Explain how code helps to solve that problem
-tried working with rio-tiler and lambda-tiler in order to pull specific tiles one by one into AWS lambda, but couldn’t figure out mercador tile coordiantes

-first we tried to upload the COG files, too large, then we tried to upload masks, but didn’t know the right coordinates, so then we mapped locally and then passed along the smaller tif files to lambda to process embarrassingly parallely


Benchmark?
