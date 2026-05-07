# Notes App - Three-Tier Architecture on AWS

This repository contains a simple Notes application demonstrating a three-tier architecture deployed on AWS. It allows users to add, view, and delete notes.

## Architecture Overview

* **Frontend:** HTML/JS application served via Nginx on an EC2 instance in a **Public Subnet**. Nginx also acts as a reverse proxy to securely route API requests to the backend.
* **Backend:** Python Flask API (`app.py`) running on an EC2 instance in a **Private Subnet**.
* **Database:** MySQL database running on an EC2 instance in a **Private Subnet**.
* **Network:** Custom VPC utilizing an Internet Gateway for public access and a NAT Gateway to allow private instances to download packages securely.

## Files Included

* `Index.html`: The frontend user interface.
* `app.py`: The Python Flask backend API.
* `README.md`: Deployment instructions.

---

## Step 1: AWS VPC & EC2 Infrastructure Setup

### 1. Networking (VPC Setup)
1. Create a custom VPC in your AWS Console.
2. Create **1 Public Subnet** (for the Frontend) and **2 Private Subnets** (for the Backend and Database).
3. Create an **Internet Gateway (IGW)** and attach it to the VPC. Add a route to the IGW in the Public Subnet's Route Table.
4. Create a **NAT Gateway** in the Public Subnet. Add a route to the NAT Gateway in the Private Subnets' Route Tables so your backend and DB instances can reach the internet for updates.

### 2. Security Groups (Firewalls)
* **Frontend SG:** Allow Inbound HTTP (Port 80) from Anywhere (0.0.0.0/0) and SSH (Port 22) from your personal IP.
* **Backend SG:** Allow Inbound Custom TCP (Port 5000) **only** from the Frontend SG. Allow SSH (Port 22) from the Frontend SG (acting as a bastion).
* **Database SG:** Allow Inbound MySQL (Port 3306) **only** from the Backend SG. Allow SSH (Port 22) from the Frontend SG.

---

## Step 2: Database Setup (Private EC2)

SSH into your Database EC2 instance (you will need to jump through your Frontend instance or use AWS Systems Manager Session Manager).

**1. Install MySQL:**
```bash
sudo apt update
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql

Install Python & Dependencies:

sudo apt update
sudo apt install python3 python3-pip python3-venv -y

Set up the Application Environment:

mkdir ~/backend && cd ~/backend
python3 -m venv venv
source venv/bin/activate
pip install Flask Flask-Cors mysql-connector-python
