create table if not exists Genre (
	GenreID serial primary key,
	GenreName varchar(50) not null unique	
);

create table if not exists Artist (
	ArtistID serial primary key,
	Name varchar(50) not null
);

create table if not exists GenresArtists (
	ID serial primary key,
	ArtistID integer references Artist(ArtistID),
	GenreID integer references Genre(GenreID)
);

create table if not exists Album (
	AlbumID serial primary key,
	AlbumName varchar(50) not null,
	Year integer not null 
	check (Year >= 1000 and Year <= 10000)
);

create table if not exists Collection(
	CollectionID serial primary key,
	Title varchar(50) not null,
	Year integer not null,
	check (Year >= 1000 and Year <= 10000)
);

create table if not exists Track (
	AlbumID integer references Album(AlbumID),
	TrackID serial primary key,
	Title varchar(50) not null,
	Time time not null
);

create table if not exists AlbumArtist(
	ID serial primary key,
	ArtistID integer references Artist(ArtistID),
	AlbumID integer references Album(AlbumID)
);

create table if not exists TrackCollection(
	ID serial primary key,
	TrackID integer references Track(TrackID),
	CollectionID integer references Collection(CollectionID)
);