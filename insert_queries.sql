

-- Insert into artworks table
INSERT INTO artworks (artist, title, year, size, current_location, description)
VALUES ('Frida Kahlo', 'Self-Portrait as a Tehuana', 1943, '76 cm x 61 cm', 'North Carolina Museum of Art', 'The original piece, Kahlo’s Self Portrait as a Tehuana, was painted the year of her divorce from fellow artist and ex-husband Diego Rivera and is said to be symbolic of her inability to stop thinking about him. It goes by two other names: Diego in My Thoughts and Thinking of Diego, and presumably makes reference to the intense dynamic between Jules and Rue in the show.');
-- Insert into scenes table
INSERT INTO scenes (series_id, artwork_id, scene_description)
VALUES ((SELECT id FROM series WHERE title = 'Euphoria'), (SELECT id FROM artworks WHERE title = 'Self-Portrait as a Tehuana'), 'Jules recreates a famous work of art by Frida Kahlo, appearing with a portrait of love interest Rue painted on her forehead.');
