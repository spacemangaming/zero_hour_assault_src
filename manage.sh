#!/bin/bash

# ─────────────────────────────────────────────────────────────────────────────
# Zero Hour Assault - Menu-Driven Server Management Utility (Python 3.12 Enforced)
# ─────────────────────────────────────────────────────────────────────────────

# Configurations
SCREEN_NAME="zhaserver"
SERVER_DIR="server"
VENV_DIR=".venv"
CONF_FILE="server/server.conf"

# ANSI Color Codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Determine Python command to use (prefer python3.12)
PYTHON_CMD="python3.12"
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3 &> /dev/null; then
    # If python3 is version 3.12, we can use it
    version_str=$(python3 -V 2>&1 | cut -d' ' -f2)
    if [[ "$version_str" =~ ^3\.12 ]]; then
        PYTHON_CMD="python3"
    fi
fi

# Helper: Print Banner
show_banner() {
    echo -e "${CYAN}=====================================================================${NC}"
    echo -e "${CYAN}${BOLD}                 ZERO HOUR ASSAULT SERVER MANAGER${NC}"
    echo -e "${CYAN}=====================================================================${NC}"
}

# Command: Install system packages via sudo (Python 3.12 specific)
install_system_deps() {
    echo -e "${BLUE}[*] Checking and installing Python 3.12 and system dependencies (requires sudo)...${NC}"
    
    # Detect package manager and install Python 3.12 specifically
    if [ -f /etc/debian_version ]; then
        echo -e "${YELLOW}[!] Debian/Ubuntu detected. Installing Python 3.12 via APT...${NC}"
        sudo apt-get update
        sudo apt-get install -y python3.12 python3.12-venv python3.12-dev screen
        PYTHON_CMD="python3.12"
    elif [ -f /etc/redhat-release ]; then
        echo -e "${YELLOW}[!] RedHat/CentOS/Fedora detected. Installing Python 3.12 via DNF/YUM...${NC}"
        sudo dnf install -y python3.12 python3.12-pip screen || sudo yum install -y python3.12 python3.12-pip screen
        PYTHON_CMD="python3.12"
    elif [ -f /etc/arch-release ]; then
        echo -e "${YELLOW}[!] Arch Linux detected. Installing Python via Pacman...${NC}"
        sudo pacman -Sy --noconfirm python python-pip screen
        # Arch usually has python pointing to latest, we check if it is 3.12+
        PYTHON_CMD="python"
    else
        echo -e "${YELLOW}[!] Unknown Linux distribution. Proceeding with default command check...${NC}"
    fi

    # Verify installation
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        # Fallback to python3 if version matches 3.12
        if command -v python3 &> /dev/null; then
            version_str=$(python3 -V 2>&1 | cut -d' ' -f2)
            if [[ "$version_str" =~ ^3\.12 ]]; then
                PYTHON_CMD="python3"
            else
                echo -e "${RED}[ERROR] python3.12 is not installed and python3 is not version 3.12 (found $version_str).${NC}"
                return 1
            fi
        else
            echo -e "${RED}[ERROR] python3.12 is not installed or not in PATH. Please install it manually.${NC}"
            return 1
        fi
    fi
    
    if ! command -v screen &> /dev/null; then
        echo -e "${RED}[ERROR] screen is still not installed. Please install it manually.${NC}"
        return 1
    fi

    echo -e "${GREEN}[OK] System dependencies and Python 3.12 are verified/installed.${NC}"
    return 0
}

# Command: Install Python dependencies
install_deps() {
    # 1. System packages (sudo)
    install_system_deps
    if [ $? -ne 0 ]; then
        return 1
    fi

    # 2. Virtual environment setup
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}[!] Virtual environment not found. Creating one with $PYTHON_CMD...${NC}"
        "$PYTHON_CMD" -m venv "$VENV_DIR"
        if [ $? -ne 0 ]; then
            echo -e "${RED}[ERROR] Failed to create virtual environment using $PYTHON_CMD.${NC}"
            return 1
        fi
        echo -e "${GREEN}[OK] Virtual environment created successfully.${NC}"
    fi

    # 3. Python package setup
    echo -e "${BLUE}[*] Activating virtual environment...${NC}"
    source "$VENV_DIR/bin/activate"

    echo -e "${BLUE}[*] Upgrading pip...${NC}"
    pip install --upgrade pip -q

    echo -e "${BLUE}[*] Installing required server packages (websockets, PyNaCl, requests)...${NC}"
    pip install websockets PyNaCl requests -q
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to install Python dependencies.${NC}"
        return 1
    fi
    echo -e "${GREEN}[OK] All Python dependencies are set up.${NC}"
    return 0
}

# Command: Start server
start_server() {
    # Install dependencies first (will skip if already done)
    install_deps
    if [ $? -ne 0 ]; then
        return
    fi

    # Check if already running
    if screen -list | grep -q "\.${SCREEN_NAME}"; then
        echo -e "${YELLOW}[!] Server is already running inside screen session '${SCREEN_NAME}'.${NC}"
        return
    fi

    # Get port from server.conf if exists
    local port=10000
    if [ -f "$CONF_FILE" ]; then
        local conf_port=$(grep -i '^port' "$CONF_FILE" | cut -d'=' -f2 | xargs)
        if [ -n "$conf_port" ]; then
            port="$conf_port"
        fi
    fi

    echo -e "${BLUE}[*] Starting server on port $port inside screen session '${SCREEN_NAME}'...${NC}"
    screen -dmS "$SCREEN_NAME" bash -c "source $VENV_DIR/bin/activate && cd $SERVER_DIR && python zhaserver.py"
    
    sleep 1.5
    if screen -list | grep -q "\.${SCREEN_NAME}"; then
        echo -e "${GREEN}[OK] Server started successfully.${NC}"
        echo -e "${BLUE}[*] Select 'Attach to Logs' from the main menu to view the console.${NC}"
    else
        echo -e "${RED}[ERROR] Failed to start server in screen. Check server logs for details.${NC}"
    fi
}

# Command: Stop server
stop_server() {
    if ! screen -list | grep -q "\.${SCREEN_NAME}"; then
        echo -e "${YELLOW}[!] No running server screen session found.${NC}"
        return
    fi

    echo -e "${BLUE}[*] Stopping server screen session '${SCREEN_NAME}'...${NC}"
    screen -XS "$SCREEN_NAME" quit
    sleep 1
    echo -e "${GREEN}[OK] Server stopped.${NC}"
}

# Command: Show Status
status_server() {
    clear
    show_banner
    echo -e "${BOLD}Server Status Information:${NC}"
    echo -e "─────────────────────────────────────────────────────────────────────"
    
    # 1. Process Status
    if screen -list | grep -q "\.${SCREEN_NAME}"; then
        echo -e "Status:         ${GREEN}${BOLD}RUNNING${NC} (Screen Session: $SCREEN_NAME)"
    else
        echo -e "Status:         ${RED}${BOLD}STOPPED${NC}"
    fi

    # 2. Config/Python Info
    local port="Default (10000)"
    if [ -f "$CONF_FILE" ]; then
        local conf_port=$(grep -i '^port' "$CONF_FILE" | cut -d'=' -f2 | xargs)
        if [ -n "$conf_port" ]; then
            port="$conf_port"
        fi
    fi
    echo -e "Listening Port: ${YELLOW}$port${NC}"
    echo -e "Config Path:    ${BLUE}$CONF_FILE${NC}"
    echo -e "Python Version: ${MAGENTA}$($PYTHON_CMD -V 2>&1)${NC}"
    echo -e "─────────────────────────────────────────────────────────────────────"
    echo
}

# Command: Configure server port
configure_server() {
    clear
    show_banner
    echo -e "${BOLD}Configure Server Settings:${NC}"
    echo -e "─────────────────────────────────────────────────────────────────────"
    local current_port=10000
    if [ -f "$CONF_FILE" ]; then
        local conf_port=$(grep -i '^port' "$CONF_FILE" | cut -d'=' -f2 | xargs)
        if [ -n "$conf_port" ]; then
            current_port="$conf_port"
        fi
    fi

    echo -e "Current port: ${YELLOW}$current_port${NC}"
    read -p "Enter new server port (1024-65535) or press Enter to keep current: " new_port
    
    if [ -z "$new_port" ]; then
        echo -e "${BLUE}No changes made.${NC}"
        return
    fi

    if [[ ! "$new_port" =~ ^[0-9]+$ ]] || [ "$new_port" -lt 1024 ] || [ "$new_port" -gt 65535 ]; then
        echo -e "${RED}[ERROR] Invalid port number.${NC}"
        return
    fi

    # Write config
    mkdir -p "$(dirname "$CONF_FILE")"
    cat << EOF > "$CONF_FILE"
# Zero Hour Assault Game Server Configuration
# Feel free to change configuration parameters below

# Server listening port
port = $new_port
EOF

    echo -e "${GREEN}[OK] server.conf updated. New port: $new_port${NC}"
}

# Command: Install Nginx reverse proxy with SSL
setup_nginx() {
    clear
    show_banner
    echo -e "${BOLD}Setup Nginx Reverse Proxy with SSL (requires sudo):${NC}"
    echo -e "─────────────────────────────────────────────────────────────────────"
    echo -e "This will install Nginx and Certbot, acquire a Let's Encrypt SSL"
    echo -e "certificate, and configure Nginx to proxy secure connections (wss://)"
    echo -e "on port 10000 to the game server running locally."
    echo
    echo -e "${YELLOW}[!] Make sure your domain name points to this VPS IP first!${NC}"
    echo
    read -p "Enter your domain name (e.g. server.example.com): " domain
    if [ -z "$domain" ]; then
        echo -e "${RED}[ERROR] Domain name cannot be empty.${NC}"
        return
    fi
    
    read -p "Enter local game server port (Nginx will proxy to this, default: 10001): " local_port
    local_port=${local_port:-10001}

    echo -e "${BLUE}[*] Installing Nginx and Certbot...${NC}"
    if [ -f /etc/debian_version ]; then
        sudo apt-get update
        sudo apt-get install -y nginx certbot python3-certbot-nginx
    elif [ -f /etc/redhat-release ]; then
        sudo dnf install -y epel-release
        sudo dnf install -y nginx certbot python3-certbot-nginx || sudo yum install -y nginx certbot
    else
        echo -e "${RED}[ERROR] Unsupported distribution. Please install Nginx/Certbot manually.${NC}"
        return
    fi

    # 1. Create temp HTTP config for Certbot validation
    echo -e "${BLUE}[*] Creating temporary HTTP Nginx config...${NC}"
    local temp_conf="/etc/nginx/sites-available/zhaserver"
    if [ ! -d "/etc/nginx/sites-available" ]; then
        temp_conf="/etc/nginx/conf.d/zhaserver.conf"
    fi

    sudo bash -c "cat << EOF > '$temp_conf'
server {
    listen 80;
    server_name $domain;
    location / {
        return 200 'OK';
    }
}
EOF"

    # Link site if sites-enabled exists
    if [ -d "/etc/nginx/sites-enabled" ]; then
        sudo ln -sf "$temp_conf" "/etc/nginx/sites-enabled/zhaserver"
    fi

    echo -e "${BLUE}[*] Restarting Nginx to load temp config...${NC}"
    sudo systemctl restart nginx

    # 2. Acquire Let's Encrypt Certificate
    echo -e "${BLUE}[*] Running Certbot to acquire SSL certificate...${NC}"
    sudo certbot certonly --nginx -d "$domain" --non-interactive --agree-tos --register-unsafely-without-email
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Certbot failed to acquire certificate. Verify domain resolution.${NC}"
        return
    fi

    # 3. Create permanent reverse proxy configuration
    echo -e "${BLUE}[*] Creating permanent reverse proxy Nginx configuration...${NC}"
    sudo bash -c "cat << EOF > '$temp_conf'
server {
    listen 80;
    server_name $domain;
    return 301 https://\$host\$request_uri;
}

server {
    listen 10000 ssl;
    server_name $domain;

    ssl_certificate /etc/letsencrypt/live/$domain/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$domain/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:$local_port;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \"Upgrade\";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
EOF"

    echo -e "${BLUE}[*] Testing Nginx configuration...${NC}"
    sudo nginx -t
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Nginx configuration test failed.${NC}"
        return
    fi

    echo -e "${BLUE}[*] Reloading Nginx...${NC}"
    sudo systemctl reload nginx

    # 4. Update server.conf port to local_port
    mkdir -p "$(dirname "$CONF_FILE")"
    cat << EOF > "$CONF_FILE"
# Zero Hour Assault Game Server Configuration
# Feel free to change configuration parameters below

# Server listening port (Proxied locally by Nginx)
port = $local_port
EOF

    echo -e "${GREEN}[OK] Nginx reverse proxy with SSL successfully set up!${NC}"
    echo -e "${YELLOW}[!] Note: Your python server has been set to run on local port $local_port.${NC}"
    echo -e "${YELLOW}[!] Make sure to restart the server from the menu to bind to the new port.${NC}"
}

# Helper: Check and toggle a role file
toggle_role_file() {
    local char_dir="$1"
    local role_file="$2"
    local role_name="$3"

    if [ -f "$char_dir/$role_file" ]; then
        rm -f "$char_dir/$role_file"
        echo -e "${RED}[-] Revoked $role_name role.${NC}"
    else
        touch "$char_dir/$role_file"
        echo -e "${GREEN}[+] Granted $role_name role.${NC}"
    fi
}

# Command: Manage Roles Submenu
manage_roles_menu() {
    clear
    show_banner
    echo -e "${BOLD}Character Role Manager:${NC}"
    echo -e "─────────────────────────────────────────────────────────────────────"
    read -p "Enter character username: " username
    
    if [ -z "$username" ]; then
        echo -e "${RED}[ERROR] Username cannot be empty.${NC}"
        return
    fi

    local char_dir="server/chars/$username"
    if [ ! -d "$char_dir" ]; then
        echo -e "${YELLOW}[!] Character '$username' does not have a folder on the server.${NC}"
        read -p "Create folder '$char_dir' now? (y/n): " create_dir
        if [[ "$create_dir" =~ ^[yY] ]]; then
            mkdir -p "$char_dir"
            echo -e "${GREEN}[OK] Created character folder.${NC}"
        else
            echo -e "${BLUE}Returning to main menu...${NC}"
            return
        fi
    fi

    while true; do
        clear
        show_banner
        echo -e "${BOLD}Manage Roles for Character:${NC} ${MAGENTA}$username${NC}"
        echo -e "─────────────────────────────────────────────────────────────────────"
        
        # Display current role status
        local is_dev="${RED}Inactive${NC}"
        local is_admin="${RED}Inactive${NC}"
        local is_mod="${RED}Inactive${NC}"
        local is_builder="${RED}Inactive${NC}"
        
        [ -f "$char_dir/developer.usr" ] && is_dev="${GREEN}ACTIVE${NC}"
        [ -f "$char_dir/admin.usr" ] && is_admin="${GREEN}ACTIVE${NC}"
        [ -f "$char_dir/moderator.usr" ] && is_mod="${GREEN}ACTIVE${NC}"
        [ -f "$char_dir/builder.usr" ] && is_builder="${GREEN}ACTIVE${NC}"

        echo -e "1) Toggle Developer Role      (Current: $is_dev)"
        echo -e "2) Toggle Administrator Role  (Current: $is_admin)"
        echo -e "3) Toggle Moderator Role      (Current: $is_mod)"
        echo -e "4) Toggle Builder Role        (Current: $is_builder)"
        echo -e "5) Finish & Return to Main Menu"
        echo -e "─────────────────────────────────────────────────────────────────────"
        read -p "Select an option [1-5]: " role_opt
        
        case "$role_opt" in
            1)
                toggle_role_file "$char_dir" "developer.usr" "Developer"
                sleep 1
                ;;
            2)
                toggle_role_file "$char_dir" "admin.usr" "Administrator"
                sleep 1
                ;;
            3)
                toggle_role_file "$char_dir" "moderator.usr" "Moderator"
                sleep 1
                ;;
            4)
                toggle_role_file "$char_dir" "builder.usr" "Builder"
                sleep 1
                ;;
            5)
                break
                ;;
            *)
                echo -e "${RED}[ERROR] Invalid option.${NC}"
                sleep 1
                ;;
        esac
    done
}

# ─────────────────────────────────────────────────────────────────────────────
# Main Loop (Menu)
# ─────────────────────────────────────────────────────────────────────────────
while true; do
    clear
    show_banner
    
    # Quick running check
    running_status="${RED}STOPPED${NC}"
    if screen -list | grep -q "\.${SCREEN_NAME}"; then
        running_status="${GREEN}RUNNING${NC}"
    fi
    
    echo -e "Server Status: $running_status"
    echo -e "─────────────────────────────────────────────────────────────────────"
    echo -e "1) Start Server"
    echo -e "2) Stop Server"
    echo -e "3) Restart Server"
    echo -e "4) View Server Status Details"
    echo -e "5) Attach to Logs (Ctrl+A then D to detach)"
    echo -e "6) Configure Port"
    echo -e "7) Manage Character Roles (dev/admin/mod/builder)"
    echo -e "8) Install / Force Reinstall Dependencies"
    echo -e "9) Setup Nginx Reverse Proxy with SSL (wss://)"
    echo -e "10) Exit"
    echo -e "─────────────────────────────────────────────────────────────────────"
    read -p "Select an option [1-10]: " main_opt
    
    case "$main_opt" in
        1)
            start_server
            read -p "Press Enter to continue..."
            ;;
        2)
            stop_server
            read -p "Press Enter to continue..."
            ;;
        3)
            stop_server
            sleep 1
            start_server
            read -p "Press Enter to continue..."
            ;;
        4)
            status_server
            read -p "Press Enter to continue..."
            ;;
        5)
            if screen -list | grep -q "\.${SCREEN_NAME}"; then
                echo -e "${BLUE}[*] Attaching to screen session '${SCREEN_NAME}'...${NC}"
                sleep 1
                screen -r "$SCREEN_NAME"
            else
                echo -e "${RED}[ERROR] Server is not running.${NC}"
                read -p "Press Enter to continue..."
            fi
            ;;
        6)
            configure_server
            read -p "Press Enter to continue..."
            ;;
        7)
            manage_roles_menu
            ;;
        8)
            install_deps
            read -p "Press Enter to continue..."
            ;;
        9)
            setup_nginx
            read -p "Press Enter to continue..."
            ;;
        10)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}[ERROR] Invalid option. Please enter a number between 1 and 10.${NC}"
            sleep 1
            ;;
    esac
done
