# Deployment Guide for DermaVision

## Prerequisites
- Node.js 20+ installed
- npm or yarn package manager
- A hosting platform account (Vercel, Replit, etc.)

## Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/kishorein25/DermaVision.git
   cd DermaVision
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:5000`

## Building for Production

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Start production server**
   ```bash
   npm start
   ```

## Deploying to Vercel

### Option 1: Using Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

### Option 2: Using GitHub Integration

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository `kishorein25/DermaVision`
4. Configure build settings:
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
5. Click "Deploy"

## Deploying to Other Platforms

### Replit
1. Import the GitHub repository to Replit
2. Replit will auto-detect the configuration from `.replit` file
3. Click "Run" to start the application

### Railway
1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select the DermaVision repository
4. Railway will auto-detect Node.js and deploy

### Render
1. Go to [Render Dashboard](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
5. Click "Create Web Service"

## Environment Variables (if needed)

Currently, the application doesn't require environment variables for basic functionality. If you need to add any:

1. Create a `.env` file in the root directory
2. Add your variables:
   ```
   NODE_ENV=production
   PORT=5000
   ```

## Post-Deployment

After deployment:
1. Test all features:
   - Skin scan functionality
   - Doctor consultation
   - Mental wellness games
   - Chatbot functionality
   - Binaural songs player
2. Verify mobile responsiveness
3. Check all navigation links
4. Test authentication flows

## Troubleshooting

### Build Fails
- Ensure all dependencies are installed: `npm install`
- Check Node.js version: `node --version` (should be 20+)
- Clear cache: `npm cache clean --force`

### Port Already in Use
- Change port in the code or use environment variable
- Kill the process using the port: `lsof -ti:5000 | xargs kill`

### Missing Dependencies
- Run: `npm install`
- For TypeScript issues: `npm install --save-dev typescript`

## Support

For issues or questions:
- **Email**: ks6700822@gmail.com
- **GitHub Issues**: Create an issue in the repository
