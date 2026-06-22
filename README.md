# TTMS Hugo Base Template

This is the base Hugo template used by the TTMS Client Provisioning Service (CPS) to create new client sites.

## Template Variables

The following placeholders will be automatically replaced when creating a new client site:

- `{{CLIENT_NAME}}` - The client's subdomain name (e.g., `sipontheave`)
- `{{SITE_TITLE}}` - The site title (e.g., "Sip on the Ave")
- `{{ANALYTICS_ID}}` - Matomo analytics site ID
- `{{WHATSAPP}}` - WhatsApp contact number
- `{{PHONE}}` - Phone contact number
- `{{EMAIL}}` - Email contact address

## Services Configuration

The template includes configuration for the following services:

### Auth Service
- User authentication and authorization
- JWT token management
- User roles and permissions

### Content Management Service (CMS)
- Menu content management
- Update UI functionality
- Configured via `params.contentManagement` (apiUrl, serviceUrl, clientId)

### Ads Service
- Advertisement management
- Client-specific ad campaigns

### Notification Service
- Push notifications (web and mobile)
- Real-time WebSocket notifications
- Notification subscriptions and delivery

All services are pre-configured with default URLs. The notification service is enabled by default and will automatically:
- Subscribe authenticated users
- Connect via WebSocket for real-time notifications
- Display notifications in the UI

See the theme documentation for notification service integration details.

## Structure

Project content and theme content are merged via Hugo module mounts: site `content/` is mounted first, then `themes/_menus_ttms/content` (dashboard, locations, api, etc.), so both project-specific and theme-provided pages are available.

```
├── content/            # Project Markdown content (menu sections, _index.md)
├── data/               # Data files (locations.yaml — replace with real locations)
├── static/             # Static assets
│   ├── _headers        # Security headers (HSTS, CORS)
│   ├── _redirects      # HTTP→HTTPS redirect
│   ├── manifest.json   # PWA manifest (name/description use {{SITE_TITLE}})
│   ├── branding/       # Logos, favicons, images
│   ├── css/            # Custom CSS (colors.css, custom.css)
│   └── js/             # Custom JavaScript
├── themes/             # Hugo theme (git submodule)
├── scripts/            # Helper scripts (e.g. register-client.sh)
├── hugo.toml           # Hugo configuration (with placeholders)
├── netlify.toml        # Netlify deployment config
└── build_menu.sh       # Build script (submodules, optional register-client, hugo build)

## Theme

The theme `_menus_ttms` is added as a git submodule from:
https://github.com/anomrac21/ttms-app-cluster (subdirectory: `_menus_ttms`)

## Usage by CPS

1. CPS clones this repository as a template
2. Replaces all `{{VARIABLE}}` placeholders with actual values
3. Updates `data/locations.yaml` with location information
4. Adds custom branding images
5. Creates a new GitHub repository
6. Deploys to Netlify

## GitHub Actions Deployment

Every client repository includes workflows under `.github/workflows/`:

| Workflow | Hosting | Trigger |
|----------|---------|---------|
| `k8s-redeploy.yml` | Kubernetes (default) | Push to `master`/`main` → `repository_dispatch` on `ttms-client-configs` |
| `deploy-netlify.yml` | Netlify (`DEPLOY_HOSTING=netlify`) | Push → build Hugo and upload zip to Netlify API |

### Kubernetes (default)

CPS sets **`HUGO_DEPLOY_TOKEN`** on the client repo **before the first push** so `k8s-redeploy.yml` can dispatch `hugo-redeploy` on [ttms-client-configs](https://github.com/anomrac21/ttms-client-configs).

The token must allow `repository_dispatch` on `ttms-client-configs`. CPS uses `HUGO_DEPLOY_TOKEN` from its environment (or falls back to `GITHUB_TOKEN`).

If an existing site fails with `Parameter token or opts.auth is required`, run the **hugo-deploy-token-inject** workflow in `ttms-app-cluster` or set `HUGO_DEPLOY_TOKEN` manually on the client repo, then re-run the failed workflow.

### Netlify

| Secret | Description |
|--------|-------------|
| `NETLIFY_AUTH_TOKEN` | Netlify personal access token with `sites:write` |
| `NETLIFY_SITE_NAME` | Netlify site slug (e.g. `ttms_clientname`) |

CPS sets these after creating the Netlify site during provisioning.

## Local Development

```bash
# Install Hugo
# Clone this repo
git clone https://github.com/anomrac21/ttms-hugo-base.git
cd ttms-hugo-base

# Initialize theme submodule
git submodule update --init --recursive

# Run Hugo dev server
hugo server -D
```

## Building

```bash
# Build for production
hugo --minify

# Or use the build script
./build_menu.sh
```

## License

Proprietary - TTMS (Trinidad & Tobago Menu Service)

