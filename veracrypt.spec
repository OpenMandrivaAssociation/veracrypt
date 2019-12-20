# comment out when not a hotfix release
%define hotfix	Update2

Summary:	Disk encryption software
Name:		veracrypt
Version:	1.24
Release:	%mkrel 7
License:	Microsoft Public License
Group:		File tools
Url:		https://veracrypt.codeplex.com
Source0:	https://github.com/veracrypt/VeraCrypt/archive/VeraCrypt_%{version}%{?hotfix:-%hotfix}.tar.gz
Patch2:		veracrypt-1.0f-2-desktop.patch
Patch3:		VeraCrypt-VeraCrypt_1.19-fix-desktop-files.patch
BuildRequires:	wxgtk-devel
BuildRequires:	makeself
BuildRequires:	nasm
BuildRequires:	pkgconfig(fuse)
BuildRequires:	imagemagick
%ifarch %{ix86} x86_64
BuildRequires:	yasm
%endif

%description
Free disk encryption software based on TrueCrypt.

%files
%{_docdir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*

#----------------------------------------------------------------------------

%prep
%setup -qn VeraCrypt-VeraCrypt_%{version}%{?hotfix:-%hotfix}
%autopatch -p1

%build
pushd src
%make_build TC_EXTRA_LFLAGS+="%{ldflags} -ldl" \
            TC_EXTRA_CXXFLAGS="%{optflags}" \
            TC_EXTRA_CFLAGS="%{optflags}" \
            NOSTRIP=1 \
            VERBOSE=1
popd

pushd src/Resources/Icons
convert VeraCrypt-16x16.xpm VeraCrypt-16x16.png
convert VeraCrypt-48x48.xpm VeraCrypt-48x48.png
convert VeraCrypt-128x128.xpm VeraCrypt-128x128.png
popd

%install
pushd src
%make_install
popd

for png in 128x128 48x48 16x16; do
  mkdir -p %{buildroot}%{_iconsdir}/hicolor/${png}/apps/
  install -m 0644 src/Resources/Icons/VeraCrypt-${png}.png %{buildroot}%{_iconsdir}/hicolor/${png}/apps/%{name}.png
done

rm -rf %{buildroot}%{_bindir}/%{name}-uninstall.sh
