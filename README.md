# Agora Edge SDK

 Agora Edge SDK is a collection of libraries and tools packaged in a way that removes the complexity of Agora Edge Applications development. The SDK is delivered in a Docker container that is also used as a development environment with all the tools pre-installed that are needed for developing Agora Edge applications. The container can run on any OS that supports Docker (Windows 10, Mac, Linux). This enables developers to quickly and efficiently write application code. Follow the instructions below to get started.
 
 Watch our Intro video for how to setup the Agora Edge SDK: https://vimeo.com/515496797

 Ready to get build an application? Checkout our Visualization how to: https://vimeo.com/515498047


Contact Agora:

  <a href="mailto:PARTNERS@AGORAIOT.COM">
    <img src="https://img.shields.io/badge/Ask-Agora-blue.svg" alt="Ask Agora">
  </a>

## Contents

- [Prerequisites](#prerequisites) 
- [Clone EdgeSDK repo](#clone-edge-sdk-repo)
- [Launch the development environment](#launch-the-development-environment)
- [Setup your dev workspace and generate your first module](#setup-your-dev-workspace-and-generate-your-first-module)
- [Setup your module local debugging](#setup-your-module-local-debugging)
- [Build module container image](#build-module-container-image)
- [Next Steps](#next-Steps)

## Prerequisites 
* Docker 
    * [Install Docker on Windows 10](https://docs.docker.com/docker-for-windows/install/)
    * [Install Docker on macOS](https://docs.docker.com/docker-for-mac/install/) 
    * [Install Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) 
* [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview)
* [VS Code - Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
* Git
    * [Git for Windows](https://git-scm.com/download/win)
    * [Git for Mac](https://git-scm.com/download/mac)
* [Azure IoT Edge - Linux Containers](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge-windows-with-linux)
* [Azure IoT Edge Quickstart](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart) 
> While going through Azure IoT Edge Quickstart, You can skip steps instructing you to install container engine and IoT Edge runtime, you already  installed them in the previous steps.
> If you already have an IoT Hub and registered a device, you can jump straight to [Deploy a module](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart#deploy-a-module)

## Clone EdgeSDK repo
1. Run PowerShell or gitbash 
1. Browse the location where you want to clone the repo e.g. C:\Users\{username}\code
1. Clone the repo
    ```powershell
    git clone  https://github.com/AgoraIOT/EdgeSDK.git
    ```
## Launch the development environment
1. Login to agorasdk.azurecr.io container registry using the read-only public credentials: 
    ```powershell
    docker login -u 17a2245e-6667-4128-b203-5a464adeef73 -p 37wRxzF_6B3HyLaQd-azJ19gd-3.uI8Z-1 agorasdk.azurecr.io 
    ```
1. Configure git:
    ```powershell
    git config --global user.email "you@example.com"
    git config --global user.name  "Your Name"
    ```
1. Launch VS Code 
1. Press F1 to open VS Code command pallet 
1. Start typing "Remote-Containers: Open Folder in Container" and press enter

<img src=images\remote_containers_open_folder.png/>

7. Browse to the location where EdgeSDK is cloned
8. Select the top directory of the repo (the parent of .devcontainer directory) and press open
9. Wait for the dev container to be built (_this can take several minutes the first time you launch the dev container_)
<img src=images\building_image.PNG/>

10. Once the build is done, VS Code will automatically remote into the container and install all the extensions needed for developing Agora Apps. You might get asked to acknowledge the installation of the extensions, you must agree
11. Wait for all extensions to be installed. If reloading VS Code is required, you will be promoted to do so

## Setup your dev workspace
You can either generate a new module or use the SDK to continue developing an existing one

### Generate a new module
1. Create a new folder for your module and cd into the newly created directory
    ```bash
    mkdir my_module && cd my_module
    ``` 
2. From the terminal in the panel at the bottom of the VS Code window (if not opened, you can open it from Terminal->New Terminal or "Ctr+Shift+`) run the following command:
    ```bash
    setup-workspace.sh
    ```
<img src=images\setup_workspace.PNG/>

3. When the workspace is completed successfully, you will see the following message: _Workspace setup is complete ..._ followed by an example showing you what to do next (which will be explained in the next couple of steps)
4. Generate your first module using genMod: 
    ```bash
    Example:
        ./genMod.sh -l py -n my_module -c MyModule -i my-module
    For more help:
        ./genMod.sh -h
    ```
5. If everything goes well with the module code generation, you should see your module build should run successfully to validate your environment and module generation. For C++ modules you should also see the unit test result.

<img src=images\cpp_build.PNG\>

6. Open the new module directory in VS Code: File -> Open Folder -> /workspace/{your module name} -> Click OK
1. Wait for the VS Code to re-launch and install all the required extensions
1. Browse the directory structure of the module in the file explorer on the left side
1. Open README.md to get description of the module directory structure and details on how to build the code 
1. The generated code has a complete sample algorithm that builds and runs as a module, explore the code and use it as starting point to develop you own
1. The complete API documentation can be found under "deps/hermes-base-cpp/doc/doxygen-cpp/html" 

### Clone an existing Agora Edge module
Follow this steps if you already have an existing Agora module you would like to continue to develop and debug in this environment
1. Form the terminal in the panel at the bottom of the VS Code window (if not opened, you can open it from Terminal->New Terminal or "Ctr+Shift+`) run the following command:
    ```bash
    git clone {your module repo URL}
    ```
    > TIP: If you are working on multiple modules or multiple feature branches of the same module, you can create one environment for each module/branch and destroy it once done.

2. Open your module directory in VSCode move on to the next step to setup local debugging for your module

## Setup your module local debugging
You need to do this one time setup to enable the use of IoT Edge Simulator to interact with your module in a local debug session without deploying the module as a container.
> Redo these steps every time you remove the dev container 
1. Connect Azure IoT Hub extension to the IoT Hub that has your dev device (command palette->Azure IoT Hub: Set IoT Hub Connection String->Enter  then enter the Hub connection string)

<img src=images\set_connection_string.png\>

2. Setup IoT Edge Simulator (command palette->Azure IoT Edge: Setup IoT Edge Simulator->Enter, then select your dev device from the list)

<img src=images\setup_simulator.png/>

3. Set module credentials in VSCode user settings (command palette->Azure IoT Edge: Set Module Credentials toUser Settings->Enter) 

<img src=images\set_cred.png/>

## Debug your module locally

Before starting a local debug session, if you have iotedge running on your host OS, stop iotedge service and remove edgeHub container:

    
   ```bash
   Windows 10, run powershell as administrator and stop the service from powershell:
      Stop-Service iotedge
   Linux:
      sudo systemctl stop iotedge
    
   Remove edgeHub:
      docker rm edgeHub
   ```

### C++/C#
1. Build your module code (command palette->Tasks: Run Build Task->Enter then select build-x86_64 from the list )

<img src=images\build_x86.png/>

2. Launch a debug session (F5 or the debug symbol on the left side) 
3. Add breakpoints and step through your code  

### Python
1. In VS Code go to debug view and select "HBM Launch" and click on launch (the green arrow)

<img src=images\py_launch_hbm.PNG/>

2. Now switch the debug config to "Python Attach" and click on the green arrow

<img src=images\py_attach.PNG/>

3. Add breakpoints and step through your Python code

<img src=images\py_debug.PNG/>

4. When done, disconnect the Python session and then stop the HBM session


## Build module container image 

1. Login to your container registry: 
    ```bash
    docker login -u {username} -p {password} url 
    ```
    > TIP: For testing out modules while actively developing, you can start a local registry using the following command: 
    > **docker run -d -p 5000:5000 --restart=always --name registry registry:2**
    > then use **localhost:5000** as a registry URL

1. Browse to build/target/x86_64/docker
1. Build the module container
    ```bash
    ./build-module.sh -r {your container registry url} -t {image tag} -p
    ``` 
1. You can add the newly built module to you Azure IoT Edge deployment and start iotedge service to see your module running (docker logs {your module name} to see debug message produced by your module)

## Browse API documentation
1. Browse to the documentation directory inside from VSCode terminal and launch Python http server at port 3032
    ```bash
    From your module top level directory:
    cd deps/hermes-base-cpp/doc/doxygen-cpp/html
    python3 -m http.server 3032 >/dev/null 2>&1 &
    ```
2. Open http://localhost:3032/ in your web browser

> Note: Python API documentation is coming soon. There is one-to-one mapping between C++ APIs and Python APIs in Agora Edge SDK. In the meantime, you can use C++ API documentation for Python until Python docs are ready.

## Next Steps
[Contact Agora](mailto:PARTNERS@AGORAIOT.COM) for some exciting real world IoT Edge use cases 
